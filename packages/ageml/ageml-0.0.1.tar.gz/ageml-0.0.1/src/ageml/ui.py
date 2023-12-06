"""Implement the user interface.

Used in the AgeML project to enable the user to enter commands
to run the modelling with desired inputs.

Classes:
--------
Interface - reads, parses and executes user commands.
CLI - reads and parsers user commands via command line.
InteractiveCLI - reads and parsers user commands via command line via an interactive interface.
"""

import argparse
import numpy as np
import pandas as pd
import os
import warnings

from datetime import datetime
from statsmodels.stats.multitest import multipletests
import scipy.stats as stats

import ageml.messages as messages
from ageml.visualizer import Visualizer
from ageml.utils import create_directory, feature_extractor, significant_markers, convert, log
from ageml.modelling import AgeML, Classifier
from ageml.processing import find_correlations


class Interface:

    """Reads, parses and executes user commands.

    This class allows the user to enter certain commands.
    These commands enable the user to run the modellin with the selected
    input files and parameters.

    Parameters
    -----------
    args: arguments with which to run the modelling

    Public methods:
    ---------------
    setup(self): Creates required directories and files to store results.

    set_visualizer(self): Set visualizer with output directory.

    set_model(self): Set model with parameters.

    set_classifier(self): Set classifier with parameters.

    check_file(self, file): Check that file exists.

    load_csv(self, file): Use panda to load csv into dataframe.

    load_data(self, required): Load data from csv files.

    age_distribution(self, dfs, labels=None): Use visualizer to show age distribution.

    features_vs_age(self, df, significance=0.05): Use visualizer to explore relationship between features and age.

    model_age(self, df, model): Use AgeML to fit age model with data.

    predict_age(self, df, model): Use AgeML to predict age with data.

    factors_vs_deltas(self, dfs_ages, dfs_factors, groups, significance=0.05): Calculate correlations between factors and deltas.

    deltas_by_group(self, df, labels): Calculate summary metrics of deltas by group.

    classify(self, df1, df2, groups): Classify two groups based on deltas.

    run_wrapper(self, run): Wrapper for running modelling with log.

    run_age(self): Run basic age modelling.

    run_lifestyle(self): Run age modelling with lifestyle factors.

    run_clinical(self): Run age modelling with clinical factors.

    run_classification(self): Run classification between two different clinical groups.
    """

    def __init__(self, args):
        """Initialise variables."""

        # Arguments with which to run modelling
        self.args = args

        # Flags
        self.flags = {"clinical": False, "covariates": False}

        # Set up directory for storage of results
        self.setup()

        # Initialise objects form library
        self.set_visualizer()
        self.set_model()
        self.set_classifier()

    def setup(self):
        """Create required directories and files to store results."""

        # Create directories
        self.dir_path = os.path.join(self.args.output, "ageml")
        if os.path.exists(self.dir_path):
            warnings.warn(
                "Directory %s already exists files may be overwritten." % self.dir_path,
                category=UserWarning,
            )
        create_directory(self.dir_path)
        create_directory(os.path.join(self.dir_path, "figures"))

        # Create .txt log file and log time
        self.log_path = os.path.join(self.dir_path, "log.txt")
        with open(self.log_path, "a") as f:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(current_time + "\n")

    def set_visualizer(self):
        """Set visualizer with output directory."""

        self.visualizer = Visualizer(self.dir_path)

    def set_model(self):
        """Set model with parameters."""

        self.ageml = AgeML(
            self.args.scaler_type,
            self.args.scaler_params,
            self.args.model_type,
            self.args.model_params,
            self.args.cv_split,
            self.args.seed,
        )

    def set_classifier(self):
        """Set classifier with parameters."""

        self.classifier = Classifier()

    def check_file(self, file):
        """Check that file exists."""
        if not os.path.exists(file):
            return False
        else:
            return True

    def load_csv(self, file):
        """Use panda to load csv into dataframe.

        Parameters
        ----------
        file: path to file; must be .csv
        """

        if file is not None:
            # Check file exists
            if not self.check_file(file):
                raise FileNotFoundError("File %s not found." % file)
            df = pd.read_csv(file, header=0, index_col=0)
            df.columns = df.columns.str.lower()  # ensure lower case
            return df
        else:
            return None

    def load_data(self, required=None):
        """Load data from csv files.

        Parameters
        ----------
        required: list of required files"""

        # Load files
        print("-----------------------------------")
        print("Loading data...")

        # Required files default
        if required is None:
            required = []

        # Load features
        self.df_features = self.load_csv(self.args.features)
        if self.df_features is not None:
            if "age" not in self.df_features.columns:
                raise KeyError(
                    "Features file must contain a column name 'age', or any other case-insensitive variation."
                )
        elif "features" in required:
            raise ValueError("Features file must be provided.")

        # Load covariates
        self.df_covariates = self.load_csv(self.args.covariates)
        if self.df_covariates is not None:
            # Check that covar name is given
            if self.args.covar_name:
                self.flags['covariates'] = True

        # Load factors
        self.df_factors = self.load_csv(self.args.factors)
        if self.df_factors is None and "factors" in required:
            raise ValueError("Factors file must be provided.")

        # Load clinical
        self.df_clinical = self.load_csv(self.args.clinical)
        if self.df_clinical is not None:
            if "cn" not in self.df_clinical.columns:
                raise KeyError(
                    "Clinical file must contian a column name 'CN' or any other case-insensitive variation."
                )
            # Check datatypes of columns are all boolean
            elif [
                self.df_clinical[col].dtype == bool for col in self.df_clinical.columns
            ].count(False) != 0:
                raise TypeError("Clinical columns must be boolean type.")
            else:
                self.flags['clinical'] = True
                self.cn_subjects = self.df_clinical[self.df_clinical["cn"]].index
        elif "clinical" in required:
            raise ValueError("Clinical file must be provided.")

        # Load ages
        # Check if already has ages loaded
        if hasattr(self, "df_ages"):
            if self.df_ages is None:
                self.df_ages = self.load_csv(self.args.ages)
            else:
                # Dont over write if None
                df = self.load_csv(self.args.ages)
                if df is not None:
                    self.df_ages = df
                    warning_message = (
                        "Ages file already loaded, overwriting with  %s provided file."
                        % self.args.ages
                    )
                    print(warning_message)
                    warnings.warn(warning_message, category=UserWarning)
        else:
            self.df_ages = self.load_csv(self.args.ages)

        # Check that ages file has required columns
        if self.df_ages is not None:
            cols = ["age", "predicted age", "corrected age", "delta"]
            for col in cols:
                if col not in self.df_ages.columns:
                    raise KeyError("Ages file must contain a column name %s" % col)

        # Remove subjects with missing values
        dfs = [
            self.df_features,
            self.df_covariates,
            self.df_factors,
            self.df_clinical,
            self.df_ages,
        ]
        labels = ['features', 'covariates', 'factors', 'clinical', 'ages']
        self.subjects_missing_data = []
        for label, df in zip(labels, dfs):
            if df is not None:
                missing_subjects = df[df.isnull().any(axis=1)].index.to_list()
                self.subjects_missing_data = (
                    self.subjects_missing_data + missing_subjects
                )
                if missing_subjects.__len__() != 0:
                    warn_message = "Subjects with missing data in %s: %s" % (label, missing_subjects)
                    print(warn_message)
                    warnings.warn(warn_message, category=UserWarning)

        # Check that all dataframes have the same subjects
        for i in range(len(dfs)):
            for j in range(len(dfs)):
                if i != j:
                    if dfs[i] is not None and dfs[j] is not None:
                        # Find subjects in one dataframe but not the other
                        non_shared_subjects = [s for s in dfs[i].index.to_list()
                                               if s not in dfs[j].index.to_list()]
                        if non_shared_subjects.__len__() != 0:
                            warn_message = ("Subjects in dataframe %s not in dataframe %s: %s"
                                            % (labels[i], labels[j], non_shared_subjects))
                            print(warn_message)
                            warnings.warn(warn_message, category=UserWarning)
                            self.subjects_missing_data = (
                                self.subjects_missing_data + non_shared_subjects
                            )

        # Remove subjects with missing values
        self.subjects_missing_data = set(self.subjects_missing_data)
        for df in dfs:
            if df is not None:
                df.drop(self.subjects_missing_data, inplace=True, errors="ignore")

    def age_distribution(self, dfs: list, labels=None, name=""):
        """Use visualizer to show age distribution.

        Parameters
        ----------
        dfs: list of dataframes with age information; shape=(n,m)
        labels: categories of separation criterion
        name: name to give to visualizer to save file"""

        # Select age information
        print("-----------------------------------")
        print("Age distribution %s" % name)
        list_ages = []
        for i, df in enumerate(dfs):
            if labels is not None:
                print(labels[i])
            ages = df["age"].to_numpy()
            print("Mean age: %.2f" % np.mean(ages))
            print("Std age: %.2f" % np.std(ages))
            print("Age range: [%d,%d]" % (np.min(ages), np.max(ages)))
            list_ages.append(ages)

        # Check that distributions of ages are similar
        print("Checking that age distributions are similar...")
        for i in range(len(list_ages)):
            for j in range(i + 1, len(list_ages)):
                _, p_val = stats.ttest_ind(list_ages[i], list_ages[j])
                if p_val < 0.05:
                    warn_message = "Age distributions %s and %s are not similar." % (
                        labels[i],
                        labels[j],
                    )
                    print(warn_message)
                    warnings.warn(warn_message, category=UserWarning)

        # Use visualiser
        self.visualizer.age_distribution(list_ages, labels, name)

    def features_vs_age(self, dfs: list, labels: list = None, significance: float = 0.05, name: str = ""):
        """Use visualizer to explore relationship between features and age.

        Parameters
        ----------
        dfs: list of dataframes with features and age; shape=(n,m+1)
        labels: # TODO
        significance: significance level for correlation"""

        # Select data to visualize
        print("-----------------------------------")
        print("Features by correlation with Age")
        print("significance: %.2g * -> FDR, ** -> bonferroni" % significance)
        if not isinstance(dfs, list):
            raise TypeError("Input to 'Interface.features_vs_age' must be a list of dataframes.")

        if labels is not None:
            print(labels)

        # Make lists to store covariate info for each dataframe
        X_list = []
        y_list = []
        corr_list = []
        order_list = []
        significance_list = []
        for df, label in zip(dfs, labels):
            # Extract features
            X, y, feature_names = feature_extractor(df)
            # Calculate correlation between features and age
            corr, order, p_values = find_correlations(X, y)
            # Reject null hypothesis of no correlation
            reject_bon, _, _, _ = multipletests(p_values, alpha=significance, method='bonferroni')
            reject_fdr, _, _, _ = multipletests(p_values, alpha=significance, method='fdr_bh')
            significant = significant_markers(reject_bon, reject_fdr)
            # Print results
            for idx, order_element in enumerate(order):
                print("%d.%s %s %s: %.2f" % (idx + 1, label, significant[order_element],
                                             feature_names[order_element], corr[order_element]))
            # Append all the values
            X_list.append(X)
            y_list.append(y)
            corr_list.append(corr)
            order_list.append(order)
            significance_list.append(significant)

        # Use visualizer to show results
        self.visualizer.features_vs_age(X_list, y_list, corr_list, order_list,
                                        significance_list, feature_names, labels, name)

    def model_age(self, df, model, name: str = ""):
        """Use AgeML to fit age model with data.

        Parameters
        ----------
        df: dataframe with features and age; shape=(n,m+1)
        model: AgeML object"""

        # Show training pipeline
        print("-----------------------------------")
        if name == "":
            print("Training Age Model")
        else:
            print("Training Model for covariate %s" % name)
        print(self.ageml.pipeline)

        # Select data to model
        X, y, _ = feature_extractor(df)

        # Fit model and plot results
        y_pred, y_corrected = model.fit_age(X, y)
        self.visualizer.true_vs_pred_age(y, y_pred, name)
        self.visualizer.age_bias_correction(y, y_pred, y_corrected, name)

        # Calculate deltas
        deltas = y_corrected - y

        # Save to dataframe and csv
        data = np.stack((y, y_pred, y_corrected, deltas), axis=1)
        cols = ["age", "predicted age", "corrected age", "delta"]
        df_ages = pd.DataFrame(data, index=df.index, columns=cols)

        return model, df_ages

    def predict_age(self, df, model):
        """Use AgeML to predict age with data."""

        # Show prediction pipeline
        print("-----------------------------------")
        print("Predicting with Age Model")
        print(self.ageml.pipeline)

        # Select data to model
        X, y, _ = feature_extractor(df)

        # Predict age
        y_pred, y_corrected = model.predict_age(X, y)

        # Calculate deltas
        deltas = y_corrected - y

        # Save to dataframe and csv
        data = np.stack((y, y_pred, y_corrected, deltas), axis=1)
        cols = ["age", "predicted age", "corrected age", "delta"]
        df_ages = pd.DataFrame(data, index=df.index, columns=cols)

        return df_ages

    def factors_vs_deltas(self, dfs_ages, dfs_factors, groups, factor_names, significance=0.05):
        """Calculate correlations between factors and deltas.

        Parameters
        ----------
        dfs_ages: list of dataframes with delta information; shape=(n,m)
        dfs_factors: list of dataframes with factor information; shape=(n,m)
        groups: list of labels for each dataframe; shape=(n,),
        factor_names: list of factor names; shape=(m,)
        significance: significance level for correlation"""

        # Select age information
        print("-----------------------------------")
        print("Correlations between lifestyle factors by group")
        print("significance: %.2g * -> FDR, ** -> bonferroni" % significance)

        # Iterate over groups
        corrs, significants = [], []
        for group, df_ages, df_factors in zip(groups, dfs_ages, dfs_factors):
            print(group)

            # Select data to visualize
            deltas = df_ages["delta"].to_numpy()
            factors = df_factors.to_numpy()

            # Calculate correlation between features and age
            corr, order, p_values = find_correlations(factors, deltas)
            corrs.append(corr)

            # Reject null hypothesis of no correlation
            reject_bon, _, _, _ = multipletests(p_values, alpha=significance, method='bonferroni')
            reject_fdr, _, _, _ = multipletests(p_values, alpha=significance, method='fdr_bh')
            significant = significant_markers(reject_bon, reject_fdr)
            significants.append(significant)

            # Print results
            for i, o in enumerate(order):
                print("%d. %s %s: %.2f" % (i + 1, significant[o], factor_names[o], corr[o]))

        # Use visualizer to show bar graph
        self.visualizer.factors_vs_deltas(corrs, groups, factor_names, significants)

    def deltas_by_group(self, df, labels):
        """Calculate summary metrics of deltas by group.
        
        Parameters
        ----------
        df: list of dataframes with delta information; shape=(n,m)
        labels: list of labels for each dataframe; shape=(n,)"""

        # Select age information
        print("-----------------------------------")
        print("Delta distribution by group")

        # Obtain deltas means and stds
        deltas = []
        for i, df_group in enumerate(df):
            deltas.append(df_group["delta"].to_numpy())
            print(labels[i])
            print("Mean delta: %.2f" % np.mean(deltas[i]))
            print("Std delta: %.2f" % np.std(deltas[i]))
            print("Delta range: [%d, %d]" % (np.min(deltas[i]), np.max(deltas[i])))

        # Obtain statistically significant difference between deltas
        print("Checking for statistically significant differences between deltas...")
        print("*: p-value < 0.01, **: p-value < 0.001")
        for i in range(len(deltas)):
            for j in range(i + 1, len(deltas)):
                _, p_val = stats.ttest_ind(deltas[i], deltas[j])
                pval_message = "p-value between %s and %s: %.2g" % (
                    labels[i],
                    labels[j],
                    p_val,
                )
                if p_val < 0.001:
                    pval_message = "*" + pval_message
                elif p_val < 0.01:
                    pval_message = "**" + pval_message
                print(pval_message)

        # Use visualizer
        self.visualizer.deltas_by_groups(deltas, labels)

    def classify(self, df1, df2, groups):
        """Classify two groups based on deltas.

        Parameters
        ----------
        df1: dataframe with delta information; shape=(n,m)
        df2: dataframe with delta information; shape=(n,m)
        groups: list of labels for each dataframe; shape=(2,)"""

        # Classification
        print("-----------------------------------")
        print("Classification between groups %s and %s" % (groups[0], groups[1]))

        # Select delta information
        deltas1 = df1["delta"].to_numpy()
        deltas2 = df2["delta"].to_numpy()

        # Create X and y for classification
        X = np.concatenate((deltas1, deltas2)).reshape(-1, 1)
        y = np.concatenate((np.zeros(deltas1.shape), np.ones(deltas2.shape)))

        # Calculate classification
        y_pred = self.classifier.fit_model(X, y)

        # Visualize AUC
        self.visualizer.classification_auc(y, y_pred, groups)

    @log
    def run_wrapper(self, run):
        """Wrapper for running modelling with log."""
        run()

    def run_age(self):
        """Run basic age modelling."""

        # Run age modelling
        print("Running age modelling...")

        # Load data
        self.load_data(required=["features"])

        # Select controls
        if self.flags["clinical"]:
            df_cn = self.df_features.loc[self.df_features.index.isin(self.cn_subjects)]
            df_clinical = self.df_features.loc[~self.df_features.index.isin(self.cn_subjects)]
        else:
            df_cn = self.df_features
            df_clinical = None

        if self.flags["covariates"] and self.args.covar_name is not None:
            # Check that covariate column exists
            if self.args.covar_name not in self.df_covariates.columns:
                raise KeyError("Covariate column %s not found in covariates file." % self.args.covar_name)

            # Create dataframe list of controls by covariate
            labels_covar = pd.unique(self.df_covariates[self.args.covar_name]).tolist()
            df_covar_cn = self.df_covariates.loc[df_cn.index]
            dfs_cn = []
            for label_covar in labels_covar:
                dfs_cn.append(df_cn[df_covar_cn[self.args.covar_name] == label_covar])

            if self.flags["clinical"]:
                # Create dataframe list of clinical cases by covariate
                df_clinical_cov = []
                for label_covar in labels_covar:
                    df_covar_clinical = self.df_covar.loc[df_clinical.index]
                    df_clinical_cov.append(df_clinical[df_covar_clinical[self.args.covar_name] == label_covar])

        else:  # No covariates, so df list of controls is [df_cn] and [df_clinical]
            dfs_cn = [df_cn]
            dfs_clinical = [df_clinical]
            labels_covar = ["all"]
            self.args.covar_name = "all"

        # Relationship between features and age
        if self.flags["covariates"]:
            initial_plots_names = f"controls_{self.args.covar_name}"
        else:
            initial_plots_names = "controls"
            
        # Use visualizer to show age distribution
        self.age_distribution(dfs_cn, labels=labels_covar, name=initial_plots_names)
    
        self.features_vs_age(dfs_cn, labels=labels_covar, name=initial_plots_names)
        
        # Model age
        self.models = {}
        dfs_ages = {}
        for label_covar, df_cn in zip(labels_covar, dfs_cn):
            model_name = f"{self.args.covar_name}_{label_covar}"
            self.models[model_name], dfs_ages[model_name] = self.model_age(df_cn, self.ageml, label_covar)
            df_ages_cn = pd.concat(dfs_ages.values(), axis=0)

        # NOTE: Matching dataframes that cannot be indexed by their name and models could be dangerous and prone to mismatches.
        # TODO: Discuss about alternatives. Use dicts for all dataframes and models?

        # Apply to clinical data
        dfs_predicted_ages = {}
        if self.flags["clinical"]:
            for df_age_clinical, label_covar in zip(dfs_clinical, labels_covar):
                model_name = f"{self.args.covar_name}_{label_covar}"
                dfs_predicted_ages[model_name] = self.predict_age(df_age_clinical, self.models[model_name])
            # Concatenate all the predicted ages
            self.df_ages = pd.concat([dfs_predicted_ages.values()])
        else:
            self.df_ages = df_ages_cn

        # Save dataframe
        if self.flags["covariates"]:
            filename = f"predicted_age_{self.args.covar_name}.csv"
        else:
            filename = "predicted_age.csv"
        self.df_ages.to_csv(os.path.join(self.dir_path, filename))

    def run_lifestyle(self):
        """Run age modelling with lifestyle factors."""

        print("Running lifestyle factors...")

        # Load data
        self.load_data(required=["factors"])

        # Run age if not ages found
        if self.df_ages is None:
            print("No age data detected...")
            print("-----------------------------------")
            self.run_age()
            print("-----------------------------------")
            print("Resuming lifestyle factors...")

        if self.flags["clinical"]:
            groups = self.df_clinical.columns.to_list()
            dfs_ages, dfs_factors = [], []
            for g in groups:
                dfs_ages.append(self.df_ages.loc[self.df_clinical[g]])
                dfs_factors.append(self.df_factors.loc[self.df_clinical[g]])
        else:
            dfs_ages = [self.df_ages]
            dfs_factors = [self.df_factors]
            groups = ["all"]

        # Calculate correlations between factors and deltas
        self.factors_vs_deltas(dfs_ages, dfs_factors, groups, self.df_factors.columns.to_list())

    def run_clinical(self):
        """Run age modelling with clinical factors."""

        print("Running clinical outcomes...")

        # Load data
        self.load_data(required=["clinical"])

        # Run age if not ages found
        if self.df_ages is None:
            print("No age data detected...")
            print("-----------------------------------")
            self.run_age()
            print("-----------------------------------")
            print("Resuming clinical outcomes...")

        # Obtain dataframes for each clinical group
        groups = self.df_clinical.columns.to_list()
        group_ages = []
        for g in groups:
            group_ages.append(self.df_ages.loc[self.df_clinical[g]])

        # Use visualizer to show age distribution
        self.age_distribution(group_ages, groups, name="clinical_groups")

        # Use visualizer to show box plots of deltas by group
        self.deltas_by_group(group_ages, groups)

    def run_classification(self):
        """Run classification between two different clinical groups."""

        print("Running classification...")

        # Load data
        self.load_data(required=["clinical"])

        # Run age if not ages found
        if self.df_ages is None:
            print("No age data detected...")
            print("-----------------------------------")
            self.run_age()
            print("-----------------------------------")
            print("Resuming clinical outcomes...")

        # Check that arguments given for each group
        if self.args.group1 is None or self.args.group2 is None:
            raise ValueError("Must provide two groups to classify.")
        
        # Check that those groups exist
        groups = [self.args.group1.lower(), self.args.group2.lower()]
        if groups[0] not in self.df_clinical.columns or groups[1] not in self.df_clinical.columns:
            raise ValueError("Classes must be one of the following: %s" % self.df_clinical.columns.to_list())

        # Obtain dataframes for each clinical group
        df_group1 = self.df_ages.loc[self.df_clinical[groups[0]]]
        df_group2 = self.df_ages.loc[self.df_clinical[groups[1]]]

        # Classify between groups
        self.classify(df_group1, df_group2, groups)


class CLI(Interface):

    """Read and parses user commands via command line.

    Public methods:
    ---------------
    configure_parser(self): Configure parser with required arguments for processing.

    configure_args(self, args): Configure argumens with required fromatting for modelling.
    """

    def __init__(self):
        """Initialise variables."""
        self.parser = argparse.ArgumentParser(
            description="Age Modelling using python.",
            formatter_class=argparse.RawTextHelpFormatter,
        )
        self.configure_parser()
        args = self.parser.parse_args()
        args = self.configure_args(args)

        # Initialise parent class
        super().__init__(args)

        # Run modelling
        case = args.run
        if case == "age":
            self.run = self.run_age
        elif case == "lifestyle":
            self.run = self.run_lifestyle
        elif case == "clinical":
            self.run = self.run_clinical
        elif case == "classification":
            self.run = self.run_classification
        else:
            raise ValueError(
                "Choose a valid run type: age, lifestyle, clinical, classification"
            )

        self.run_wrapper(self.run)

    def configure_parser(self):
        """Configure parser with required arguments for processing."""
        self.parser.add_argument(
            "-r",
            "--run",
            metavar="RUN",
            default="age",
            required=True,
            help=messages.run_long_description,
        )
        self.parser.add_argument(
            "-o",
            "--output",
            metavar="DIR",
            required=True,
            help=messages.output_long_description,
        )
        self.parser.add_argument(
            "-f", "--features", metavar="FILE", help=messages.features_long_description
        )
        self.parser.add_argument(
            "-m",
            "--model",
            nargs="*",
            default=["linear"],
            help=messages.model_long_description,
        )
        self.parser.add_argument(
            "-s",
            "--scaler",
            nargs="*",
            default=["standard"],
            help=messages.scaler_long_description,
        )
        self.parser.add_argument(
            "--cv",
            nargs="+",
            type=int,
            default=[5, 0],
            help=messages.cv_long_description,
        )
        self.parser.add_argument(
            "--covariates", metavar="FILE", help=messages.covar_long_description
        )
        self.parser.add_argument(
            "--covar_name", metavar="COVAR_NAME", help=messages.covar_name_long_description
        )
        self.parser.add_argument(
            "--factors", metavar="FILE", help=messages.factors_long_description
        )
        self.parser.add_argument(
            "--clinical", metavar="FILE", help=messages.clinical_long_description
        )
        self.parser.add_argument(
            "--systems", metavar="FILE", help=messages.systems_long_description
        )
        self.parser.add_argument(
            "--ages", metavar="FILE", help=messages.ages_long_description
        )
        self.parser.add_argument(
            "--groups", metavar="GROUP", nargs=2, help=messages.groups_long_description
        )

    def configure_args(self, args):
        """Configure argumens with required fromatting for modelling.

        Parameters
        ----------
        args: arguments object from parser
        """

        # Set CV params first item is the number of CV splits
        if len(args.cv) == 1:
            args.cv_split = args.cv[0]
            args.seed = self.parser.get_default("cv")[1]
        elif len(args.cv) == 2:
            args.cv_split, args.seed = args.cv
        else:
            raise ValueError("Too many values to unpack")

        # Set Scaler parameters first item is the scaler type
        # The rest of the arguments conform a dictionary for **kwargs
        args.scaler_type = args.scaler[0]
        if len(args.scaler) > 1:
            scaler_params = {}
            for item in args.scaler[1:]:
                # Check that item has one = to split
                if item.count("=") != 1:
                    raise ValueError(
                        "Scaler parameters must be in the format param1=value1 param2=value2 ..."
                    )
                key, value = item.split("=")
                value = convert(value)
                scaler_params[key] = value
            args.scaler_params = scaler_params
        else:
            args.scaler_params = {}

        # Set Model parameters first item is the model type
        # The rest of the arguments conform a dictionary for **kwargs
        args.model_type = args.model[0]
        if len(args.model) > 1:
            model_params = {}
            for item in args.model[1:]:
                # Check that item has one = to split
                if item.count("=") != 1:
                    raise ValueError(
                        "Model parameters must be in the format param1=value1 param2=value2 ..."
                    )
                key, value = item.split("=")
                value = convert(value)
                model_params[key] = value
            args.model_params = model_params
        else:
            args.model_params = {}

        # Set groups
        if args.groups is not None:
            args.group1, args.group2 = args.groups
        else:
            args.group1, args.group2 = None, None

        return args


class InteractiveCLI(Interface):

    """Read and parses user commands via command line via an interactive interface

    Public methods:
    ---------------

    initial_command(self): Ask for initial inputs for initial setup.

    get_line(self): Prints a prompt for the user and updates the user entry.

    force_command(self, func, command = None): Force the user to enter a valid command.

    command_interface(self): Reads in the commands and calls the corresponding
                             functions.

    cv_command(self): Loads CV parameters.

    help_command(self): Prints a list of valid commands.

    load_command(self): Loads file paths.

    model_command(self): Loads model parameters.

    output_command(self): Loads output directory.

    run_command(self): Runs the modelling.

    scaler_command(self): Loads scaler parameters.
    """

    def __init__(self):
        """Initialise variables."""

        # Initialization
        self.args = argparse.Namespace()

        # Print welcome message
        print(messages.emblem)
        print("Age Modelling (AgeML): interactive command line user interface.")

        # Setup
        print(messages.setup_banner)
        print("For Optional or Default values leave empty. \n")
        self.initial_command()

        # Configure Interface
        self.configFlag = False
        while not self.configFlag:
            try:
                print("\n Configuring Interface...")
                super().__init__(self.args)
                self.configFlag = True
            except Exception as e:
                print(e)
                print("Error configuring interface, please try again.")
                self.initial_command()

        # Run command interface
        print("\n Initialization finished.")
        print(messages.modelling_banner)
        self.command_interface()

    def initial_command(self):
        """Ask for initial inputs for initial setup."""

        # Askf for output directory
        print("Output directory path (Required):")
        self.force_command(self.output_command, "o", required=True)
        # Ask for input files
        print("Input features file path (Required for run age):")
        self.force_command(self.load_command, "l --features")
        print("Input covariates file path (Optional):")
        self.force_command(self.load_command, "l --covariates")
        print("Input factors file path (Reqruired for run lifestyle):")
        self.force_command(self.load_command, "l --factors")
        print(
            "Input clinical file path (Required for run clinical or run classification):"
        )
        self.force_command(self.load_command, "l --clinical")
        print("Input systems file path (Optional):")
        self.force_command(self.load_command, "l --systems")
        print("Input ages file path (Optional):")
        self.force_command(self.load_command, "l --ages")

        # Ask for scaler, model and CV parameters
        print("Scaler type and parameters (Default:standard):")
        self.force_command(self.scaler_command, "s")
        print("Model type and parameters (Default:linear):")
        self.force_command(self.model_command, "m")
        print("CV parameters (Default: nº splits=5 and seed=0):")
        self.force_command(self.cv_command, "cv")

    def get_line(self, required=True):
        """Print prompt for the user and update the user entry."""
        self.line = input("#: ")
        while self.line == "" and required:
            print("Must provide a value.")
            self.line = input("#: ")

    def force_command(self, func, command, required=False):
        """Force the user to enter a valid command."""
        while True:
            self.get_line(required=required)
            if self.line == "":
                self.line = "None"
            self.line = command + " " + self.line
            error = func()
            if error is None:
                return None
            else:
                print(error)

    def command_interface(self):
        """Read the command entered and call the corresponding function."""

        # Interactive mode after setup
        print("Enter 'h' for help.")
        self.get_line()  # get the user entry
        command = self.line.split()[0]  # read the first item
        while command != "q":
            error = None
            if command == "cv":
                error = self.cv_command()
            elif command == "h":
                self.help_command()
            elif command == "l":
                error = self.load_command()
            elif command == "m":
                error = self.model_command()
            elif command == "o":
                error = self.output_command()
            elif command == "r":
                error = self.run_command()
            elif command == "s":
                error = self.scaler_command()
            else:
                print("Invalid command. Enter 'h' for help.")

            # Check error and if not make updates
            if error is not None:
                print(error)
            elif command == "r":
                # Capture any error raised and print
                try:
                    self.run_wrapper(self.run)
                except Exception as e:
                    print(e)
                    print("Error running modelling.")
            elif command == "o":
                try:
                    self.setup()
                    self.set_visualizer()
                except Exception as e:
                    print(e)
                    print("Error setting up output directory.")
            elif command in ["cv", "m", "s"]:
                try:
                    self.set_model()
                except Exception as e:
                    print(e)
                    print("Error setting up model.")

            # Get next command
            self.get_line()  # get the user entry
            command = self.line.split()[0]  # read the first item

    def cv_command(self):
        """Load CV parameters."""

        # Split into items and remove  command
        self.line = self.line.split()[1:]
        error = None

        # Check that at least one argument input
        if len(self.line) == 0:
            error = "Must provide at least one argument or None."
            return error

        # Set default values
        if self.line[0] == "None":
            self.args.cv_split = 5
            self.args.seed = 0
            return error

        # Check wether items are integers
        for item in self.line:
            if not item.isdigit():
                error = "CV parameters must be integers"
                return error

        # Set CV parameters
        if len(self.line) == 1:
            self.args.cv_split = int(self.line[0])
            self.args.seed = 0
        elif len(self.line) == 2:
            self.args.cv_split, self.args.seed = int(self.line[0]), int(self.line[1])
        else:
            error = "Too many values to unpack."

        return error

    def help_command(self):
        """Print a list of valid commands."""

        # Print possible commands
        print("User commands:")
        print(messages.cv_command_message)
        print(messages.help_command_message)
        print(messages.load_command_message)
        print(messages.model_command_message)
        print(messages.output_command_message)
        print(messages.quit_command_message)
        print(messages.run_command_message)
        print(messages.scaler_command_message)

    def load_command(self):
        """Load file paths."""

        # Split into items and remove  command
        self.line = self.line.split()[1:]
        error = None

        # Determine if correct number of arguments and check file valid
        if len(self.line) > 2:
            error = "Too many arguments only two arguments --file_type and file path."
        elif len(self.line) == 1:
            error = "Must provide a file path or None when using --file_type."
        elif len(self.line) == 0:
            error = "Must provide a file type and file path."
        else:
            file_type = self.line[0]
            file = self.line[1]
            # Set file path
            if file == "None":
                file = None
            else:
                if not self.check_file(file):
                    error = "File %s not found." % file
                elif file_type in [
                    "--features",
                    "--covariates",
                    "--factors",
                    "--clinical",
                    "--ages",
                ]:
                    if not file.endswith(".csv"):
                        error = "File %s must be a .csv file." % file
                elif file_type == "--systems":
                    if not file.endswith(".txt"):
                        error = "File %s must be a .txt file." % file

        # Throw error if detected
        if error is not None:
            return error

        # Set file path
        if file_type == "--features":
            self.args.features = file
        elif file_type == "--covariates":
            self.args.covariates = file
        elif file_type == "--factors":
            self.args.factors = file
        elif file_type == "--clinical":
            self.args.clinical = file
        elif file_type == "--systems":
            self.args.systems = file
        elif file_type == "--ages":
            self.args.ages = file
        else:
            error = "Choose a valid file type: --features, --covariates, --factors, --clinical, --systems, --ages"

        return error

    def model_command(self):
        """Load model parameters."""

        # Split into items and remove  command
        self.line = self.line.split()[1:]
        valid_types = ["linear"]
        error = None

        # Check that at least one argument input
        if len(self.line) == 0:
            error = "Must provide at least one argument or None."
            return error
        else:
            model_type = self.line[0]

        # Set model type or default
        if model_type == "None":
            self.args.model_type = "linear"
        else:
            if model_type not in valid_types:
                error = "Choose a valid model type: {}".format(valid_types)
            else:
                self.args.model_type = model_type

        # Set model parameters
        if len(self.line) > 1 and model_type != "None":
            model_params = {}
            for item in self.line[1:]:
                # Check that item has one = to split
                if item.count("=") != 1:
                    error = "Model parameters must be in the format param1=value1 param2=value2 ..."
                    return error
                key, value = item.split("=")
                value = convert(value)
                model_params[key] = value
            self.args.model_params = model_params
        else:
            self.args.model_params = {}

        return error

    def output_command(self):
        """Load output directory."""

        # Split into items and remove  command
        self.line = self.line.split()[1:]
        error = None

        # Check wether there is a path
        if len(self.line) == 0:
            error = "Must provide a path."
            return error

        # Check that path exists
        path = self.line[0]
        if len(self.line) > 1:
            error = "Too many arguments only one single path."
        elif os.path.isdir(path):
            self.args.output = path
        else:
            error = "Directory %s does not exist." % path

        return error

    def run_command(self):
        """Run the modelling."""
        error = None

        # Split into items and remove  command
        self.line = self.line.split()[1:]

        # Check that at least one argument given
        if len(self.line) < 1:
            error = "Must provide at least one argument."
            return error
        elif len(self.line) > 1 and self.line[0] in ['age', 'lifestyle', 'clinical']:
            error = "Too many arguments given for run type %s" % self.line[0]
            return error
        elif len(self.line) != 3 and self.line[0] in ['classification']:
            error = "For run type %s two arguments should be given" % self.line[0]
            return error

        # Run specificed modelling
        case = self.line[0]
        if case == "age":
            self.run = self.run_age
        elif case == "lifestyle":
            self.run = self.run_lifestyle
        elif case == "clinical":
            self.run = self.run_clinical
        elif case == "classification":
            self.run = self.run_classification
            self.args.group1 = self.line[1]
            self.args.group2 = self.line[2]
        else:
            error = "Choose a valid run type: age, lifestyle, clinical, classification"

        return error

    def scaler_command(self):
        """Load scaler parameters."""

        # Split into items and remove  command
        self.line = self.line.split()[1:]
        error = None
        valid_types = ["standard"]

        # Check that at least one argument input
        if len(self.line) == 0:
            error = "Must provide at least one argument or None."
            return error
        else:
            scaler_type = self.line[0]

        # Set scaler type or default
        if scaler_type == "None":
            self.args.scaler_type = "standard"
        else:
            if scaler_type not in valid_types:
                error = "Choose a valid scaler type: {}".format(valid_types)
            else:
                self.args.scaler_type = scaler_type

        # Set scaler parameters
        if len(self.line) > 1 and scaler_type != "None":
            scaler_params = {}
            for item in self.line[1:]:
                if item.count("=") != 1:
                    error = "Scaler parameters must be in the format param1=value1 param2=value2 ..."
                    return error
                key, value = item.split("=")
                value = convert(value)
                scaler_params[key] = value
            self.args.scaler_params = scaler_params
        else:
            self.args.scaler_params = {}

        return error
