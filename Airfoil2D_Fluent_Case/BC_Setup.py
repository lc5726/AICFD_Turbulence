from math import *
import sys
mach = float(sys.argv[1])
AoA = float(sys.argv[2])
Vmag = mach*sqrt(1.4*287.1*300)
Vx = Vmag*cos(AoA/57.1)
Vy = Vmag*sin(AoA/57.1)

Script = '''/file/set-tui-version "20.2"

/file/read-case results/Airfoil2d_db.cas
/define/boundary-conditions/set/velocity-inlet inlet () velocity-spec no yes quit 
/define/boundary-conditions/set/velocity-inlet inlet () direction-0 no %.2f quit 
/define/boundary-conditions/set/velocity-inlet inlet () direction-1 no %.2f quit 
/solve/initialize/initialize-flow 
/solve/iterate 3000
/file/export/ascii total_bc_%.2f_%.2f interior-part1:002 () no x-velocity y-velocity () yes quit


/solve/cell-registers/add "airfoil" quit
/solve/cell-registers/edit "airfoil" type boundary boundary-list airfoil () quit quit
/mesh/modify-zones/ sep-cell-zone-mark fluid-part1 airfoil yes quit
/file/export/ascii airfoil_bc_%.2f_%.2f interior-part1:002 () no x-velocity () yes quit

/solve/cell-registers/add "inlet" quit
/solve/cell-registers/edit "inlet" type boundary boundary-list inlet () quit quit
/mesh/modify-zones/ sep-cell-zone-mark fluid-part1 inlet yes quit
/file/export/ascii inlet_bc_%.2f_%.2f interior-part1:017 () no x-velocity () yes quit

/solve/cell-registers/add "outlet" quit
/solve/cell-registers/edit "outlet" type boundary boundary-list outlet () quit quit
/mesh/modify-zones/ sep-cell-zone-mark fluid-part1 outlet yes quit
/file/export/ascii outlet_bc_%.2f_%.2f interior-part1:023 () no x-velocity () yes quit

/exit'''%(Vx,Vy,AoA,mach,AoA,mach,AoA,mach,AoA,mach)

with open('fluent_run.jou','w') as o:
    o.write(Script)

