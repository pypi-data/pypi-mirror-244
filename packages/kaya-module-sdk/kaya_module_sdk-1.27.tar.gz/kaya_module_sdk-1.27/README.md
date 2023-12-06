# Kaya Module SDK

[ **Description** ]: The Python3 SDK is a subcomponent of the Kaya Module
    Packer (KMP), but is deployed standalone to PyPI as it and can be
    individually installed using pip. It's purpose is to help Morty write custom
    Kaya modules stress free :) or at least - as stress free as one could
    possibly write instructions for processing complex financial data that will
    be playing with his wallet.

[ **Setup** ]: Installing SDK dependencies with the help of the Build WizZard -

    ~$ sudo ./build.sh --setup

[ **Test** ]: Running all SDK autotesters with the help of the Build WizZard -

    ~$ ./build.sh --test

[ **Check** ]: Check source files make use of type hints and adhere to PEP8 -

    ~$ ./build.sh --check

[ **Build** ]: Building, installing and publishing distribution packages -

    # Building creates the source and binary distribution files. If the build
    # wizzard script is not customized, BUILD is ON by default, so there's no
    # need to specify it when running the wizzard.

    ~$ ./build.sh
    ~$ ./build.sh BUILD

    # Installing the freshly built source distribution archive.

    ~$ ./build.sh INSTALL

    # Build WizZard actions are cumulative, and are always executed in the
    # following order if specified (BUILD -> INSTALL -> PUBLISH). In this
    # example we are building, installing and the publishing the SDK to PyPI.

    ~$ ./build.sh INSTALL PUBLISH

[ **Cleanup** ]: Remove files and directories created during the build process,
__pycache__ directories, and clear out logs with a timestamp.

    ~$ ./build.sh --cleanup

[ **Example** ]: Using Build WizZard to test, check code type hints, build,
install and publish the SDK package to PyPI -

    ~$ ./build.sh --test --check BUILD INSTALL PUBLISH

[ **Example** ]: Using the SDK to build a strategy module -

    from kaya.sdk import (
        KTimeSeries, KList, KInt, KFloat, KString,
        Module, run
    )


    class MyModule(Module):

        def __init__(self,) -> None:
            self.dummy_time_series = KTimeSeries[float]

        def main(self, args: int, debug: bool = False) -> float:
            return float(sum(args))

[ **Example** ]: Using the SDK to run a strategy module -

    from kaya_module_sdk.sdk import run
    from my_module import MyModule

    module_instance = MyModule()
    run(module_instance, args=(1,2,3,4,), kwargs={'debug': True})




