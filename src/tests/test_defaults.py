from emcpy.plots import VariableSpecs


def test_defaults_gdas_variable_specs():
    # read YAML file stored in cfg/
    # print some output
    # temperature
    varspecs = VariableSpecs(variable='temperature',
                             eval_type='magnitude')
    print(varspecs.name)
    print(varspecs.sname)
    print(varspecs.type)
    print(varspecs.range)
