# MCAKE
## Maya scripts lib

To get started:
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
