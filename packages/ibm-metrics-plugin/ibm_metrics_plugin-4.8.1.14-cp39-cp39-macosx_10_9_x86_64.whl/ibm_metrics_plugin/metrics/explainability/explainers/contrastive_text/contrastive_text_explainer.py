
# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# © Copyright IBM Corp. 2021, 2022  All Rights Reserved.
# US Government Users Restricted Rights -Use, duplication or disclosure restricted by 
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

from ibm_metrics_plugin.common.utils.constants import ExplainabilityMetricType, InputDataType, ProblemType
from ibm_metrics_plugin.common.utils.metrics_logger import MetricLogger
from ibm_metrics_plugin.common.utils.python_utils import convert_to_pandas
from ibm_metrics_plugin.metrics.explainability.entity.explain_config import ExplainConfig
from ibm_metrics_plugin.metrics.explainability.explainers.base_explainer import BaseExplainer

from aix360i.algorithms.cem_text.cem_text import CEMtext

import pandas as pd

from ibm_metrics_plugin.metrics.explainability.util.model_wrapper import ModelWrapper

logger = MetricLogger(__name__)


class ContrastiveTextExplainer(BaseExplainer):
    """
    Class to get explanation using protodash explainer
    """

    def __init__(self, explain_config: ExplainConfig):
        super().__init__(explain_config)
        self.initialize()

    def is_supported(self):
        if self.config.input_data_type is InputDataType.TEXT and self.config.problem_type is not ProblemType.REGRESSION \
                and ExplainabilityMetricType.CONTRASTIVE_TEXT in self.config.metric_types:
            return True

        return False

    def validate(self):
        missing_values = []
        if(self.config.label_column is None):
            missing_values.append("class_labels")

        # if(self.config.prediction_column is None):
        #     missing_values.append("prediction_column")

        if(self.config.features is None or len(self.config.features) == 0):
            missing_values.append("feature_columns")

        if(len(missing_values) > 0):
            raise AttributeError(
                "Missing inputs .Details :{}".format(missing_values))


    def initialize(self):
        #Check for support
        if not self.is_supported():
            raise Exception("Contrastive text explainer support is available only for text classification models")

        #Validate the inputs
        self.validate()
        self.class_labels = self.config.class_labels
        self.feature_columns = self.config.features
        print("In validate features are :{}".format(self.feature_columns))

        #Check for inputs
        ir_parameters = self.config.parameters
        self.use_ir_results = True
        self.use_words_ranked = False
        self.use_ir = True
        self.use_ir = ir_parameters.get("use_input_reduction")
        self.important_words = []
        if self.use_ir:
            self.use_words_ranked = ir_parameters.get("words_ranked")
            if not self.use_words_ranked:
                self.use_ir_results = ir_parameters.get("ir_result")
            else:
                self.use_ir_results = False
        else:
            #Get the important_words list 
            self.words_list = self.config.parameters.get("words_list")
            if self.words_list is None:
                self.words_list = []



    def explain(self, data, scoring_fn):
        explanations = []
        if scoring_fn is None:
            raise ValueError("scoring_fn is required for executing contrastive anamoly explanations.")
        if data is None:
            raise ValueError("Input data is None. Please provide a valid data frame.")

        data_df = convert_to_pandas(data)
        self.scoring_fn = ModelWrapper(score_fn=scoring_fn).score
        for row in data_df[self.feature_columns].values:
            cem_text_rsp = self.explain_row(row)
            explanations.append(cem_text_rsp)

        result = {
            "local_explanations":explanations
        }

        return result

    def explain_row(self,data_row):
        cem_text = CEMtext(self.scoring_fn,self.class_labels,feature_columns=self.feature_columns)
        cem_text_rsp = cem_text.explain_instance(data_row[0],word_list=self.words_list,info=True)
        return self.__format_explanation(cem_text_rsp)


    def __format_explanation(self,cem_text_rsp):
        return cem_text_rsp