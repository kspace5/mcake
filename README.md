# MCAKE
## Maya scripts lib

# To Get started
Just get 'mcake' folder cloned from git to maya scripts path, as in `C:\Users\zyx\Documents\maya\2022\scripts`

# For Creating a Biped Rig in Maya
First create an HIK character.  
Then import the UI builder  
```
import mcake.rigging.biped_rig_ui as br
br.createRiggingToolsUI()
```

## Earlier notes (deprecated)
```
import mcake.generic_utils.base as gu
reload(gu)
#gu.rename_selected_by_replace("g_","g_mq_")
#gu.freeze_and_center()
#gu.zero_x_pivot()
gu.duplicate_and_mirror_x()

# For Biped Rig
import mcake.rigging.controls as rct
reload(br)
br.createRiggingToolsUI()
```
