import copy
import io
import logging
from dataclasses import dataclass
from functools import reduce
from operator import add
from pathlib import Path
from typing import ClassVar, Collection, Dict, List, Optional, Sequence, Set, TextIO, Union

import pandas as pd
from rhoknp import BasePhrase, Document
from rhoknp.cohesion import (
    Argument,
    ArgumentType,
    EndophoraArgument,
    ExophoraArgument,
    ExophoraReferent,
    ExophoraReferentType,
    Predicate,
)

from cohesion_tools.extractors import BridgingExtractor, CoreferenceExtractor, PasExtractor

logger = logging.getLogger(__name__)


class CohesionScorer:
    """A class to evaluate system output.

    To evaluate system output with this class, you have to prepare gold data and system prediction data as instances of
    :class:`rhoknp.Document`

    Args:
        exophora_referent_types: 評価の対象とする外界照応の照応先 (rhoknp.cohesion.ExophoraReferentTypeType を参照)
        pas_cases: 述語項構造の評価の対象とする格 (rhoknp.cohesion.rel.CASE_TYPES を参照)
        pas_verbal: 述語項構造解析において用言を述語として扱うかどうか (default: True)
        pas_nominal: 述語項構造解析において体言を述語として扱うかどうか (default: True)
        bridging: 橋渡し照応の評価を行うかどうか (default: False)
        coreference: 共参照の評価を行うかどうか (default: False)
    """

    ARGUMENT_TYPE2ANALYSIS: ClassVar[Dict[ArgumentType, str]] = {
        ArgumentType.CASE_EXPLICIT: "overt",
        ArgumentType.CASE_HIDDEN: "dep",
        ArgumentType.OMISSION: "zero_endophora",
        ArgumentType.EXOPHORA: "exophora",
    }

    def __init__(
        self,
        exophora_referent_types: Collection[ExophoraReferentType],
        pas_cases: Collection[str],
        pas_verbal: bool = True,
        pas_nominal: bool = True,
        bridging: bool = False,
        coreference: bool = False,
    ) -> None:
        self.exophora_referent_types: List[ExophoraReferentType] = list(exophora_referent_types)
        self.pas_cases: List[str] = list(pas_cases)
        self.pas_verbal: bool = pas_verbal
        self.pas_nominal: bool = pas_nominal
        self.bridging: bool = bridging
        self.coreference: bool = coreference

    def run(self, predicted_documents: Sequence[Document], gold_documents: Sequence[Document]) -> "CohesionScore":
        """読み込んだ正解文書集合とシステム予測文書集合に対して評価を行う

        Args:
            predicted_documents: システム予測文書集合
            gold_documents: 正解文書集合

        Returns:
            CohesionScore: 評価結果のスコア
        """
        # long document may have been ignored
        assert {d.doc_id for d in predicted_documents} <= {d.doc_id for d in gold_documents}
        doc_ids: List[str] = [d.doc_id for d in predicted_documents]
        doc_id2predicted_document: Dict[str, Document] = {d.doc_id: d for d in predicted_documents}
        doc_id2gold_document: Dict[str, Document] = {d.doc_id: d for d in gold_documents}

        comp_result: Dict[tuple, str] = {}
        sub_scorers: List[SubCohesionScorer] = []
        results = []
        for doc_id in doc_ids:
            sub_scorer = SubCohesionScorer(
                doc_id2predicted_document[doc_id],
                doc_id2gold_document[doc_id],
                exophora_referent_types=self.exophora_referent_types,
                pas_cases=self.pas_cases,
                pas_verbal=self.pas_verbal,
                pas_nominal=self.pas_nominal,
                bridging=self.bridging,
                coreference=self.coreference,
            )
            results.append(sub_scorer.run())
            sub_scorers.append(sub_scorer)
            comp_result.update({(doc_id, *k): v for k, v in sub_scorer.comp_result.items()})
        return reduce(add, results)


class SubCohesionScorer:
    """Scorer for single document pair.

    Args:
        predicted_document: システム予測文書
        gold_document: 正解文書
        exophora_referent_types: 評価の対象とする外界照応の照応先
        pas_cases: 述語項構造の評価の対象とする格
        pas_verbal: 述語項構造解析において用言を述語として扱うかどうか (default: True)
        pas_nominal: 述語項構造解析において体言を述語として扱うかどうか (default: True)
        bridging: 橋渡し照応の評価を行うかどうか (default: False)
        coreference: 共参照の評価を行うかどうか (default: False)

    Attributes:
        doc_id: 対象の文書ID
        predicted_document: システム予測文書
        gold_document: 正解文書
        exophora_referent_types: 評価の対象とする外界照応の照応先
        pas_cases: 評価の対象となる格
        pas: 述語項構造の評価を行うかどうか
        bridging: 橋渡し照応の評価を行うかどうか
        coreference: 共参照の評価を行うかどうか
        predicted_pas_predicates: システム予測文書に含まれる述語
        predicted_bridging_anaphors: システム予測文書に含まれる橋渡し照応詞
        predicted_mentions: システム予測文書に含まれるメンション
        gold_pas_predicates: 正解文書に含まれる述語
        gold_bridging_anaphors: 正解文書に含まれる橋渡し照応詞
        gold_mentions: 正解文書に含まれるメンション
        comp_result: 正解と予測を比較した結果を格納するための辞書
    """

    def __init__(
        self,
        predicted_document: Document,
        gold_document: Document,
        exophora_referent_types: Collection[ExophoraReferentType],
        pas_cases: Collection[str],
        pas_verbal: bool,
        pas_nominal: bool,
        bridging: bool,
        coreference: bool,
    ) -> None:
        assert predicted_document.doc_id == gold_document.doc_id
        self.doc_id: str = gold_document.doc_id
        self.predicted_document: Document = predicted_document
        self.gold_document: Document = gold_document

        self.exophora_referent_types: List[ExophoraReferentType] = list(exophora_referent_types)
        self.pas_cases: List[str] = list(pas_cases)
        self.pas: bool = len(pas_cases) > 0 and (pas_verbal or pas_nominal)
        self.bridging: bool = bridging
        self.coreference: bool = coreference

        self.predicted_pas_predicates: List[Predicate] = []
        self.predicted_bridging_anaphors: List[Predicate] = []
        self.predicted_mentions: List[BasePhrase] = []
        for base_phrase in predicted_document.base_phrases:
            if PasExtractor.is_pas_target(base_phrase, verbal=pas_verbal, nominal=pas_nominal):
                self.predicted_pas_predicates.append(base_phrase.pas.predicate)
            if self.bridging is True and BridgingExtractor.is_bridging_target(base_phrase):
                self.predicted_bridging_anaphors.append(base_phrase.pas.predicate)
            if self.coreference is True and CoreferenceExtractor.is_coreference_target(base_phrase):
                self.predicted_mentions.append(base_phrase)

        self.gold_pas_predicates: List[Predicate] = []
        self.gold_bridging_anaphors: List[Predicate] = []
        self.gold_mentions: List[BasePhrase] = []
        for base_phrase in gold_document.base_phrases:
            self.gold_pas_predicates.append(base_phrase.pas.predicate)
            if self.bridging is True:
                self.gold_bridging_anaphors.append(base_phrase.pas.predicate)
            if self.coreference is True:
                self.gold_mentions.append(base_phrase)

        self.comp_result: Dict[tuple, str] = {}

    def run(self) -> "CohesionScore":
        """Perform evaluation for the given gold document and system prediction document.

        Returns:
            CohesionScore: 評価結果のスコア
        """
        self.comp_result.clear()
        pas_metrics = self._evaluate_pas() if self.pas is True else None
        bridging_metrics = self._evaluate_bridging() if self.bridging is True else None
        coreference_metric = self._evaluate_coreference() if self.coreference is True else None
        return CohesionScore(pas_metrics, bridging_metrics, coreference_metric)

    def _evaluate_pas(self) -> pd.DataFrame:
        """Compute predicate-argument structure analysis scores"""
        metrics = pd.DataFrame(
            [[Metrics() for _ in CohesionScorer.ARGUMENT_TYPE2ANALYSIS.values()] for _ in self.pas_cases],
            index=self.pas_cases,
            columns=list(CohesionScorer.ARGUMENT_TYPE2ANALYSIS.values()),
        )
        global_index2predicted_pas_predicate: Dict[int, Predicate] = {
            p.base_phrase.global_index: p for p in self.predicted_pas_predicates
        }
        global_index2gold_pas_predicate: Dict[int, Predicate] = {
            p.base_phrase.global_index: p for p in self.gold_pas_predicates
        }

        for global_index in range(len(self.predicted_document.base_phrases)):
            for pas_case in self.pas_cases:
                if predicted_pas_predicate := global_index2predicted_pas_predicate.get(global_index):
                    predicted_pas_arguments = predicted_pas_predicate.pas.get_arguments(pas_case, relax=False)
                    predicted_pas_arguments = self._filter_arguments(predicted_pas_arguments, predicted_pas_predicate)
                else:
                    predicted_pas_arguments = []
                # this project predicts one argument for one predicate
                assert len(predicted_pas_arguments) in (0, 1)

                if gold_pas_predicate := global_index2gold_pas_predicate.get(global_index):
                    gold_pas_arguments = gold_pas_predicate.pas.get_arguments(pas_case, relax=False)
                    gold_pas_arguments = self._filter_arguments(gold_pas_arguments, gold_pas_predicate)
                    relaxed_gold_pas_arguments = gold_pas_predicate.pas.get_arguments(
                        pas_case,
                        relax=True,
                        include_nonidentical=True,
                    )
                    if pas_case == "ガ":
                        relaxed_gold_pas_arguments += gold_pas_predicate.pas.get_arguments(
                            "判ガ",
                            relax=True,
                            include_nonidentical=True,
                        )
                    relaxed_gold_pas_arguments = self._filter_arguments(relaxed_gold_pas_arguments, gold_pas_predicate)
                else:
                    gold_pas_arguments = relaxed_gold_pas_arguments = []

                key = (global_index, pas_case)

                # compute precision
                if len(predicted_pas_arguments) > 0:
                    predicted_pas_argument = predicted_pas_arguments[0]
                    if predicted_pas_argument in relaxed_gold_pas_arguments:
                        relaxed_gold_pas_argument = relaxed_gold_pas_arguments[
                            relaxed_gold_pas_arguments.index(predicted_pas_argument)
                        ]
                        # use argument_type of gold argument if possible
                        analysis = CohesionScorer.ARGUMENT_TYPE2ANALYSIS[relaxed_gold_pas_argument.type]
                        self.comp_result[key] = analysis
                        metrics.loc[pas_case, analysis].tp += 1
                    else:
                        # system出力のargument_typeはgoldのものと違うので不整合が起きるかもしれない
                        analysis = CohesionScorer.ARGUMENT_TYPE2ANALYSIS[predicted_pas_argument.type]
                        self.comp_result[key] = "wrong"  # precision が下がる
                    metrics.loc[pas_case, analysis].tp_fp += 1

                # compute recall
                # 正解が複数ある場合、そのうち一つが当てられていればそれを正解に採用
                if (
                    len(gold_pas_arguments) > 0
                    or self.comp_result.get(key) in CohesionScorer.ARGUMENT_TYPE2ANALYSIS.values()
                ):
                    recalled_pas_argument: Optional[Argument] = None
                    for relaxed_gold_pas_argument in relaxed_gold_pas_arguments:
                        if relaxed_gold_pas_argument in predicted_pas_arguments:
                            recalled_pas_argument = relaxed_gold_pas_argument  # 予測されている項を優先して正解の項に採用
                            break
                    if recalled_pas_argument is not None:
                        analysis = CohesionScorer.ARGUMENT_TYPE2ANALYSIS[recalled_pas_argument.type]
                        assert self.comp_result[key] == analysis
                    else:
                        # いずれも当てられていなければ、relax されていない項から一つを選び正解に採用
                        analysis = CohesionScorer.ARGUMENT_TYPE2ANALYSIS[gold_pas_arguments[0].type]
                        if len(predicted_pas_arguments) > 0:
                            assert self.comp_result[key] == "wrong"
                        else:
                            self.comp_result[key] = "wrong"  # recall が下がる
                    metrics.loc[pas_case, analysis].tp_fn += 1
        return metrics

    def _filter_arguments(self, arguments: List[Argument], predicate: Predicate) -> List[Argument]:
        filtered = []
        for orig_argument in arguments:
            argument = copy.copy(orig_argument)
            if argument.case.endswith("≒"):
                argument.case = argument.case[:-1]
            if argument.case == "判ガ":
                argument.case = "ガ"
            if argument.case == "ノ？":
                argument.case = "ノ"
            if isinstance(argument, ExophoraArgument):
                argument.exophora_referent.index = None  # 「不特定:人１」なども「不特定:人」として扱う
                if argument.exophora_referent.type not in self.exophora_referent_types:
                    continue
            else:
                assert isinstance(argument, EndophoraArgument)
                # filter out self-anaphora
                if argument.base_phrase == predicate.base_phrase:
                    continue
                # filter out cataphora
                if (
                    argument.base_phrase.global_index > predicate.base_phrase.global_index
                    and argument.base_phrase.sentence.sid != predicate.base_phrase.sentence.sid
                ):
                    continue
            filtered.append(argument)
        return filtered

    def _evaluate_bridging(self) -> pd.Series:
        """Compute bridging reference resolution scores"""
        metrics: Dict[str, Metrics] = {anal: Metrics() for anal in ("dep", "zero_endophora", "exophora")}
        global_index2predicted_anaphor: Dict[int, Predicate] = {
            p.base_phrase.global_index: p for p in self.predicted_bridging_anaphors
        }
        global_index2gold_anaphor: Dict[int, Predicate] = {
            p.base_phrase.global_index: p for p in self.gold_bridging_anaphors
        }

        for global_index in range(len(self.predicted_document.base_phrases)):
            if global_index in global_index2predicted_anaphor:
                predicted_anaphor = global_index2predicted_anaphor[global_index]
                predicted_antecedents: List[Argument] = self._filter_arguments(
                    predicted_anaphor.pas.get_arguments("ノ", relax=False),
                    predicted_anaphor,
                )
            else:
                predicted_antecedents = []
            # this project predicts one antecedent for one anaphor
            assert len(predicted_antecedents) in (0, 1)

            if global_index in global_index2gold_anaphor:
                gold_anaphor: Predicate = global_index2gold_anaphor[global_index]
                gold_antecedents: List[Argument] = self._filter_arguments(
                    gold_anaphor.pas.get_arguments("ノ", relax=False),
                    gold_anaphor,
                )
                relaxed_gold_antecedents: List[Argument] = gold_anaphor.pas.get_arguments(
                    "ノ",
                    relax=True,
                    include_nonidentical=True,
                )
                relaxed_gold_antecedents += gold_anaphor.pas.get_arguments("ノ？", relax=True, include_nonidentical=True)
                relaxed_gold_antecedents = self._filter_arguments(relaxed_gold_antecedents, gold_anaphor)
            else:
                gold_antecedents = relaxed_gold_antecedents = []

            key = (global_index, "ノ")

            # compute precision
            if len(predicted_antecedents) > 0:
                predicted_antecedent = predicted_antecedents[0]
                if predicted_antecedent in relaxed_gold_antecedents:
                    # use argument_type of gold antecedent if possible
                    relaxed_gold_antecedent = relaxed_gold_antecedents[
                        relaxed_gold_antecedents.index(predicted_antecedent)
                    ]
                    analysis = CohesionScorer.ARGUMENT_TYPE2ANALYSIS[relaxed_gold_antecedent.type]
                    if analysis == "overt":
                        analysis = "dep"
                    self.comp_result[key] = analysis
                    metrics[analysis].tp += 1
                else:
                    analysis = CohesionScorer.ARGUMENT_TYPE2ANALYSIS[predicted_antecedent.type]
                    if analysis == "overt":
                        analysis = "dep"
                    self.comp_result[key] = "wrong"
                metrics[analysis].tp_fp += 1

            # calculate recall
            if gold_antecedents or (self.comp_result.get(key, None) in CohesionScorer.ARGUMENT_TYPE2ANALYSIS.values()):
                recalled_antecedent: Optional[Argument] = None
                for relaxed_gold_antecedent in relaxed_gold_antecedents:
                    if relaxed_gold_antecedent in predicted_antecedents:
                        recalled_antecedent = relaxed_gold_antecedent  # 予測されている先行詞を優先して正解の先行詞に採用
                        break
                if recalled_antecedent is not None:
                    analysis = CohesionScorer.ARGUMENT_TYPE2ANALYSIS[recalled_antecedent.type]
                    if analysis == "overt":
                        analysis = "dep"
                    assert self.comp_result[key] == analysis
                else:
                    analysis = CohesionScorer.ARGUMENT_TYPE2ANALYSIS[gold_antecedents[0].type]
                    if analysis == "overt":
                        analysis = "dep"
                    if len(predicted_antecedents) > 0:
                        assert self.comp_result[key] == "wrong"
                    else:
                        self.comp_result[key] = "wrong"
                metrics[analysis].tp_fn += 1
        return pd.Series(metrics)

    def _evaluate_coreference(self) -> pd.Series:
        """Compute coreference resolution scores"""
        metrics: Dict[str, Metrics] = {anal: Metrics() for anal in ("endophora", "exophora")}
        global_index2predicted_mention: Dict[int, BasePhrase] = {p.global_index: p for p in self.predicted_mentions}
        global_index2gold_mention: Dict[int, BasePhrase] = {p.global_index: p for p in self.gold_mentions}
        for global_index in range(len(self.predicted_document.base_phrases)):
            if predicted_mention := global_index2predicted_mention.get(global_index):
                predicted_other_mentions = self._filter_mentions(predicted_mention.get_coreferents(), predicted_mention)
                predicted_exophora_referents = self._filter_exophora_referents(
                    [e.exophora_referent for e in predicted_mention.entities if e.exophora_referent is not None],
                )
            else:
                predicted_other_mentions = []
                predicted_exophora_referents = set()

            if gold_mention := global_index2gold_mention.get(global_index):
                gold_other_mentions = self._filter_mentions(
                    gold_mention.get_coreferents(include_nonidentical=False),
                    gold_mention,
                )
                relaxed_gold_other_mentions = self._filter_mentions(
                    gold_mention.get_coreferents(include_nonidentical=True),
                    gold_mention,
                )
                gold_exophora_referents = self._filter_exophora_referents(
                    [e.exophora_referent for e in gold_mention.entities if e.exophora_referent is not None],
                )
                relaxed_gold_exophora_referents = self._filter_exophora_referents(
                    [e.exophora_referent for e in gold_mention.entities_all if e.exophora_referent is not None],
                )
            else:
                gold_other_mentions = relaxed_gold_other_mentions = []
                gold_exophora_referents = relaxed_gold_exophora_referents = set()

            key = (global_index, "=")

            # compute precision
            if predicted_other_mentions or predicted_exophora_referents:
                if any(mention in relaxed_gold_other_mentions for mention in predicted_other_mentions):
                    analysis = "endophora"
                    self.comp_result[key] = analysis
                    metrics[analysis].tp += 1
                elif predicted_exophora_referents & relaxed_gold_exophora_referents:
                    analysis = "exophora"
                    self.comp_result[key] = analysis
                    metrics[analysis].tp += 1
                else:
                    analysis = "endophora" if predicted_other_mentions else "exophora"
                    self.comp_result[key] = "wrong"
                metrics[analysis].tp_fp += 1

            # compute recall
            if gold_other_mentions or gold_exophora_referents or self.comp_result.get(key) in ("endophora", "exophora"):
                if any(mention in relaxed_gold_other_mentions for mention in predicted_other_mentions):
                    analysis = "endophora"
                    assert self.comp_result[key] == analysis
                elif predicted_exophora_referents & relaxed_gold_exophora_referents:
                    analysis = "exophora"
                    assert self.comp_result[key] == analysis
                else:
                    analysis = "endophora" if gold_other_mentions else "exophora"
                    self.comp_result[key] = "wrong"
                metrics[analysis].tp_fn += 1
        return pd.Series(metrics)

    @staticmethod
    def _filter_mentions(other_mentions: List[BasePhrase], mention: BasePhrase) -> List[BasePhrase]:
        """Filter out cataphora mentions"""
        return [
            another_mention for another_mention in other_mentions if another_mention.global_index < mention.global_index
        ]

    def _filter_exophora_referents(self, exophora_referents: List[ExophoraReferent]) -> Set[str]:
        filtered = set()
        for orig_exophora_referent in exophora_referents:
            exophora_referent = copy.copy(orig_exophora_referent)
            exophora_referent.index = None
            if exophora_referent.type in self.exophora_referent_types:
                filtered.add(exophora_referent.text)
        return filtered


@dataclass(frozen=True)
class CohesionScore:
    """A data class for storing the numerical result of an evaluation"""

    pas_metrics: Optional[pd.DataFrame]
    bridging_metrics: Optional[pd.Series]
    coreference_metrics: Optional[pd.Series]

    def to_dict(self) -> Dict[str, Dict[str, "Metrics"]]:
        """Convert data to dictionary"""
        df_all = pd.DataFrame(index=["all_case"])
        if self.pas is True:
            assert self.pas_metrics is not None
            df_pas: pd.DataFrame = self.pas_metrics.copy()
            df_pas["overt_dep"] = df_pas["overt"] + df_pas["dep"]
            df_pas["endophora"] = df_pas["overt"] + df_pas["dep"] + df_pas["zero_endophora"]
            df_pas["zero"] = df_pas["zero_endophora"] + df_pas["exophora"]
            df_pas["dep_zero"] = df_pas["dep"] + df_pas["zero"]
            df_pas["all"] = df_pas["overt"] + df_pas["dep_zero"]
            df_all = pd.concat([df_pas, df_all])
            df_all.loc["all_case"] = df_pas.sum(axis=0)

        if self.bridging is True:
            assert self.bridging_metrics is not None
            df_bar = self.bridging_metrics.copy()
            df_bar["endophora"] = df_bar["dep"] + df_bar["zero_endophora"]
            df_bar["zero"] = df_bar["zero_endophora"] + df_bar["exophora"]
            df_bar["dep_zero"] = df_bar["dep"] + df_bar["zero"]
            df_bar["all"] = df_bar["dep_zero"]
            df_all.loc["bridging"] = df_bar

        if self.coreference is True:
            assert self.coreference_metrics is not None
            df_coref = self.coreference_metrics.copy()
            df_coref["all"] = df_coref["endophora"] + df_coref["exophora"]
            df_all.loc["coreference"] = df_coref

        return {
            k1: {k2: v2 for k2, v2 in v1.items() if pd.notna(v2)} for k1, v1 in df_all.to_dict(orient="index").items()
        }

    def export_txt(self, destination: Union[str, Path, TextIO]) -> None:
        """Export the evaluation results in a text format.

        Args:
            destination (Union[str, Path, TextIO]): 書き出す先
        """
        lines = []
        for rel, analysis2metric in self.to_dict().items():
            lines.append(f"{rel}格" if (self.pas_metrics is not None) and (rel in self.pas_metrics.index) else rel)
            for analysis, metric in analysis2metric.items():
                lines.append(f"  {analysis}")
                lines.append(f"    precision: {metric.precision:.4f} ({metric.tp}/{metric.tp_fp})")
                lines.append(f"    recall   : {metric.recall:.4f} ({metric.tp}/{metric.tp_fn})")
                lines.append(f"    F        : {metric.f1:.4f}")
        text = "\n".join(lines) + "\n"

        if isinstance(destination, (Path, str)):
            Path(destination).write_text(text)
        elif isinstance(destination, io.TextIOBase):
            destination.write(text)

    def export_csv(self, destination: Union[str, Path, TextIO], sep: str = ",") -> None:
        """Export the evaluation results in a csv format.

        Args:
            destination: 書き出す先
            sep: 区切り文字 (default: ',')
        """
        result_dict = self.to_dict()
        text = "task" + sep
        columns: List[str] = list(result_dict["all_case"].keys())
        text += sep.join(columns) + "\n"
        for task, measures in result_dict.items():
            text += task + sep
            text += sep.join(f"{measures[column].f1:.6}" if column in measures else "" for column in columns)
            text += "\n"

        if isinstance(destination, (Path, str)):
            Path(destination).write_text(text)
        elif isinstance(destination, io.TextIOBase):
            destination.write(text)

    @property
    def pas(self) -> bool:
        """Whether self includes the score of predicate-argument structure analysis."""
        return self.pas_metrics is not None

    @property
    def bridging(self) -> bool:
        """Whether self includes the score of bridging anaphora resolution."""
        return self.bridging_metrics is not None

    @property
    def coreference(self) -> bool:
        """Whether self includes the score of coreference resolution."""
        return self.coreference_metrics is not None

    def __add__(self, other: "CohesionScore") -> "CohesionScore":
        if self.pas is True:
            assert self.pas_metrics is not None
            assert other.pas_metrics is not None
            pas_metrics = self.pas_metrics + other.pas_metrics
        else:
            pas_metrics = None
        if self.bridging is True:
            assert self.bridging_metrics is not None
            assert other.bridging_metrics is not None
            bridging_metrics = self.bridging_metrics + other.bridging_metrics
        else:
            bridging_metrics = None
        if self.coreference is True:
            assert self.coreference_metrics is not None
            assert other.coreference_metrics is not None
            coreference_metric = self.coreference_metrics + other.coreference_metrics
        else:
            coreference_metric = None
        return CohesionScore(pas_metrics, bridging_metrics, coreference_metric)


@dataclass
class Metrics:
    """A data class to calculate and represent F-score"""

    tp_fp: int = 0
    tp_fn: int = 0
    tp: int = 0

    def __add__(self, other: "Metrics") -> "Metrics":
        return Metrics(self.tp_fp + other.tp_fp, self.tp_fn + other.tp_fn, self.tp + other.tp)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        return (self.tp_fp == other.tp_fp) and (self.tp_fn == other.tp_fn) and (self.tp == other.tp)

    @property
    def precision(self) -> float:
        if self.tp_fp == 0:
            return 0.0
        return self.tp / self.tp_fp

    @property
    def recall(self) -> float:
        if self.tp_fn == 0:
            return 0.0
        return self.tp / self.tp_fn

    @property
    def f1(self) -> float:
        if (self.tp_fp + self.tp_fn) == 0:
            return 0.0
        return (2 * self.tp) / (self.tp_fp + self.tp_fn)
