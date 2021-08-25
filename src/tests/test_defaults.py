from emcpy.plots import VariableSpecs


def test_defaults_gdas_variable_specs():
    # read YAML file stored in cfg/
    # print some output
    print('--- Reading Temperature Defaults For Magnitude ---')
    # temperature
    varspecs = VariableSpecs(variable='temperature',
                             eval_type='magnitude')
    print(f'Name:          {varspecs.name}')
    print(f'Short Name:    {varspecs.sname}')
    print(f'Variable Type: {varspecs.type}')
    print(f'Colormap:      {varspecs.cmap}')
    print(f'VMin:          {varspecs.vmin}')
    print(f'VMax:          {varspecs.vmax}')
