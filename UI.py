import os
import sys
import procedural_city_generation
donemessage = "\n"+(150*"-")+"\n\t\t\t  Done, waiting for command\n"+(150*"-")+"\n"
errormessage = "\n"+(150*"-")+"\n\t\t\t  Exception Caught, Re-run\n"+(150*"-")+"\n"
path = os.path.dirname(procedural_city_generation.__file__)
sys.path.append(path)
if not os.path.exists(path+"/temp/"):
    os.system("mkdir "+path+"/temp")
if not os.path.exists(path+"/outputs/"):
    os.system("mkdir "+path+"/outputs")


def setup_matplotlib():
    """
    This function is used to set the matplotlib backend correctly.

    Parameters
    ----------

    Returns
    --------
    None

    :return:
    """
    if sys.version[0] == "3":
        import matplotlib
        try:
            matplotlib.use("Qt4Agg")
        except:
            print("PyQt4 is not installed - outputs will only be saved as images and not be visible at runtime")
            print("However, it is strongly recommended that you install PyQt4 in order to use the GUI")
            matplotlib.use("agg")


from procedural_city_generation.roadmap import main as roadmap_main
from procedural_city_generation.polygons import main as polygons_main
from procedural_city_generation.building_generation import main as building_generation_main
from procedural_city_generation.additional_stuff.Singleton import Singleton


def setRoadmapGUI(gui):
    roadmap_main.gui = gui
    Singleton("roadmap").kill()


def setPolygonsGUI(gui):
    polygons_main.gui = gui
    Singleton("polygons").kill()


def setBuilding_generationGUI(gui):
    building_generation_main.gui = gui
    Singleton("building_generation").kill()


def roadmap():
    try:
        Singleton("roadmap").kill()
        roadmap_main.submain()
    except Exception:
        import traceback, warnings
        warnings.warn(":warning: exception caught")
        traceback.print_exc()
        print(errormessage)
    else:
        print(donemessage)
    finally:
        Singleton("roadmap").kill()


def polygons():
    try:
        Singleton("polygons").kill()
        polygons_main.submain()
    except Exception:
        import traceback, warnings
        warnings.warn(":warning: exception caught")
        traceback.print_exc()
        print(errormessage)
    else:
        print(donemessage)
    finally:
        Singleton("polygons").kill()


def building_generation():
    try:
        building_generation_main.submain()
    except Exception:
        import traceback, warnings
        warnings.warn(":warning: exception caught")
        traceback.print_exc()
        print(errormessage)
    else:
        print(donemessage)
    finally:
        Singleton("building_generation").kill()


def visualization():
    os.system("blender --python "+path+"/visualization/blenderize.py")
    from procedural_city_generation.additional_stuff.Singleton import Singleton
    Singleton("visualization").kill()


def main(args):
    """

    Welcome to procedural_city_generation, a module for procedurally generating a 3D model of a city in Blender with python.

    A call to this module from the command line should follow this format::

        python UI.py <submodule-name> <options>

    <submodule-name> is either "roadmap", "polygons", "building_generation, "visualization".
    <options> is either "run" or "configure"

    If you want to configure a paremeter, go with

        python UI.py <submodule-name> --configure <parameter-name> <new value>

    """
    if len(args) == 1:
        print(main.__doc__)
        return 0
    if "configure" in args[2]:
        config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   "procedural_city_generation/inputs/{0}.conf".format(args[1]))
        if len(args) == 3:
            os.system("nano {0}".format(config_file))
            sys.exit(0)

        elif args[3] and args[4]:
            import json
            with open(config_file, 'r') as f:
                wb = json.loads(f.read())
            i = 0
            while True:
                try:
                    old = wb[args[3+i]]['value']
                    wb[args[3+i]]['value'] = eval(args[4+i])
                    print("{0} was changed from {1} to {2}".format(args[3+i], old, args[4+i]))
                    i += 2
                    if len(args)-1 < i+4:
                        break

                except:
                    print(i, len(args))
                    print("Either {0} is not a configurable parameter for {1}".format(args[3+i], args[1]))
                    return 0

            with open(config_file, 'w') as f:
                f.write(json.dumps(wb, indent=2))

            return 0

    elif "run" in args[2]:
        setup_matplotlib()
        eval(args[1])()

if __name__ == '__main__':
    main(sys.argv)
