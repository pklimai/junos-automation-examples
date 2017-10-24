
from junos import Junos                # type 'classobj'
from junos import Junos_Context        # type 'dict'
from junos import Junos_Configuration  # type 'lxml.etree._Element'
import jcs

def main():

    root = Junos_Configuration
    
    message = " - Permission all is assigned to invalid class"
    
    for element in root.findall("./system/login/class[permissions='all']"):
        jcs.emit_warning("class: " + element.find("name").text + message)
        
if __name__ == "__main__":
    main()
