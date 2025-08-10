class ModuleExecutors:
    ICICI_DIRECT_MF_EXCEL = "icici_direct_mf_excel_converter"
    KFIN_EXCEL = "kfin_excel_to_record_converter"
    ICICI_DIRECT_EQUITY_LTCG_EXCEL = "icici_direct_equity_excel_converter"

    @staticmethod
    def execute(module_name):
        if module_name == ModuleExecutors.ICICI_DIRECT_MF_EXCEL:
            from converters.icici_direct_mf_excel_converter import execute
            execute()
        elif module_name == ModuleExecutors.KFIN_EXCEL:
            from converters.kfin_excel_to_record_converter import convert_kfin_excel
            return convert_kfin_excel
        elif module_name == ModuleExecutors.ICICI_DIRECT_EQUITY_LTCG_EXCEL:
            from converters.icici_direct_equity_excel_converter import execute
            execute()
        else:
            raise ValueError(f"Unknown module name: {module_name}")