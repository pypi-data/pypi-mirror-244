from compare_datasets.prepare import PrepareForComparison
from compare_datasets.string_comparisons import StringComparisons
from compare_datasets.numeric_comparisons import NumericComparisons
from compare_datasets.datetime_comparison import DateTimeComparisons
from compare_datasets.boolean_comparison import BooleanComparisons
from compare_datasets.jaccard_similarity import JaccardSimilarity
from compare_datasets.structure import stringify_result
from compare_datasets.html_report import generate_body
from datetime import datetime
from tqdm import tqdm
from jinja2 import Template
class Compare:
    def __init__ (self, tested, expected, key=None, verbose=False, low_memory=False):
        self.verbose = verbose
        self.progress_bar = tqdm(total=100,desc="Preparing datasets", bar_format="{desc}: {percentage:2.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")
        self.progress_bar.update(5)
        self.data = PrepareForComparison(tested, expected, key, verbose=verbose, progress_bar=self.progress_bar, low_memory=low_memory)       
        self.result = [self.data.result]
        self.jaccard_similarity = JaccardSimilarity(prepared_data=self.data, verbose=self.data.verbose, progress_bar=self.progress_bar) 
        self.progress_bar.update(10)
        self.tested = self.data.tested
        self.expected = self.data.expected
        
        if len(self.data.column_list["String Columns"]) != 0:        
            self.string_comparisons = StringComparisons(prepared_data=self.data, verbose=self.data.verbose,progress_bar=self.progress_bar)
            self.result.append(self.string_comparisons.result)
        
        self.progress_bar.update(20)        

        if len(self.data.column_list["Numeric Columns"]) != 0:
            self.numeric_comparisons = NumericComparisons(prepared_data=self.data, verbose=self.data.verbose, progress_bar=self.progress_bar)
            self.result.append(self.numeric_comparisons.result)
            
        if len(self.data.column_list["Datetime Columns"]) != 0:
            self.date_comparisons = DateTimeComparisons(prepared_data=self.data, verbose=self.data.verbose, progress_bar=self.progress_bar)
            self.result.append(self.date_comparisons.result)    
            
        if len(self.data.column_list["Boolean Columns"]) != 0:
            self.boolean_comparisons = BooleanComparisons(prepared_data=self.data, verbose=self.data.verbose, progress_bar=self.progress_bar)
            self.result.append(self.boolean_comparisons.result)        
            
        self.progress_bar.update(20)
        self.progress_bar.set_description("Comparison Completed Successfully. Please print the object to view the report")
        self.progress_bar.close()
 
        
    def report (self):
        report = []
        report.append("COMPARISON REPORT\n=================")
        report.append(f"OVERALL RESULT: {stringify_result(all(self.result))}")
        report.append(self.data.__str__())
        report.append(self.jaccard_similarity.__str__())
        if len(self.data.column_list["String Columns"]) != 0:
            report.append(self.string_comparisons.__str__())
        if len(self.data.column_list["Numeric Columns"]) != 0:
            report.append(self.numeric_comparisons.__str__())
        if len(self.data.column_list["Datetime Columns"]) != 0:
            report.append(self.date_comparisons.__str__())
        if len(self.data.column_list["Boolean Columns"]) != 0:
            report.append(self.boolean_comparisons.__str__())
        return "\n \n".join(report)
        
    def __repr__ (self):
        return self.report()

      
    def get_report (self, format='txt', save_at_path=None):     
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"report_{timestamp}.{format}"
        if format == 'text':
            report = self.report()   
        if format == 'html':
            data = {'content': generate_body(self), 'analysis':''}
            if self.verbose:
                print(data)
            with open("compare_datasets/statics/report_template.html", "r") as f:
                template = Template(f.read())
            report = template.render(data)        
        if not save_at_path is None:        
            with open(f"{save_at_path}/{filename}", "w",encoding="utf-8") as f:
                f.write(report)
        return report
            

