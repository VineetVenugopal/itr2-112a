class ConverterExecutor:
    ICICI_DIRECT_MF_EXCEL = "icici_direct_mf_excel_converter"
    KFIN_EXCEL = "kfin_excel_to_record_converter"
    ICICI_DIRECT_EQUITY_LTCG_EXCEL = "icici_direct_equity_excel_converter"

    @staticmethod
    def execute(module_name):
        if module_name == ConverterExecutor.ICICI_DIRECT_MF_EXCEL:
            from .icici_direct_mf_excel_converter import execute
            execute()
        elif module_name == ConverterExecutor.ICICI_DIRECT_EQUITY_LTCG_EXCEL:
            from .icici_direct_equity_excel_converter import execute
            execute()
        else:
            raise ValueError(f"Unknown module name: {module_name}")