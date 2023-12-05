# __main__.py

import sys
import os
import argparse
import numpy as np
from .CEScore  import CEScore 
def main():
    parser = argparse.ArgumentParser("Calculate CEScore")
    CE = CEScore()
    
    parser.add_argument(
        "-s",
        "--s_score_only",
        action='store_true',
        #default=False,
        help='the model will return Sscore only',
    )
    
    parser.add_argument(
        "-m",
        "--m_score_only",
        action='store_true',
        default=False,
        help='the model will return Mscore only',
    )

    parser.add_argument(
        "-g",
        "--g_score_only",
        action='store_true',
        default=False,
        help='the model will return Gscore only',
    )

    parser.add_argument(
        "-e",
        "--ce_score_only",
        action='store_true',
        default=False,
        help='the model will return CEscore only',
    )
    
    parser.add_argument(
        "-r",
        "--ref",
        type=str,
        required=True,
        help="reference (complex texts) file path or a string",
    )
    parser.add_argument(
        "-c",
        "--cand",
        type=str,
        required=True,
        help="candidate (simplified texts) file path or a string",
    )

    parser.add_argument(
        "-o",
        "--outs",
        type=str,
        default='CEscore.res',
        help="results (scores) file path, if not provided the default file will be CEscore.res ",
    )

    args = parser.parse_args()

    if os.path.isfile(args.ref):
        with open(args.ref) as Cf:
            comps = [line.strip() for line in Cf]


        if os.path.isfile(args.cand):
            with open(args.cand) as Sf:
                simps = [line.strip() for line in Sf]

                       
            if len(comps) != len(simps):
                print(f"# of simplified texts in ({args.cand}) doesn't match the # of complex texts in ({args.ref})")
                return 1

            results=[]
            Sscore=[]
            Mscore=[]
            Gscore=[]
            CEscore=[]
            for comp,simp in zip(comps,simps):
               SS,MS,GS,CES=CE.CEScore(comp,simp)
               Sscore.append(SS) 
               Mscore.append(MS)
               Gscore.append(GS)
               CEscore.append(CES)

            if args.s_score_only:
                print(f'corpus Sscore = {np.mean(Sscore):.6}')
                for SS in Sscore:
                    results.append(f"{SS:9.6}\n")
                with open(args.outs,'w') as outFile:
                    outFile.writelines("  S_score \n")
                    outFile.writelines(results)
            elif args.m_score_only:
                print(f'corpus Mscore = {np.mean(Mscore):.6}')
                for MM in Mscore:
                    results.append(f"{MM:9.6}\n")
                with open(args.outs,'w') as outFile:
                    outFile.writelines("  M_score \n")
                    outFile.writelines(results)
            elif args.g_score_only:
                print(f'corpus Gscore = {np.mean(Gscore):.6}')
                for GG in Gscore:
                    results.append(f"{GG:9.6}\n")
                with open(args.outs,'w') as outFile:
                    outFile.writelines("  G_score \n")
                    outFile.writelines(results)

            elif args.ce_score_only:
                print(f'corpus CEscore = {np.mean(CEscore):.6}')
                for CES in CEscore:
                    results.append(f"{CES:9.6}\n")
                with open(args.outs,'w') as outFile:
                    outFile.writelines("  CE_score \n")
                    outFile.writelines(results)
            else:
                print(f'corpus Sscore = {np.mean(Sscore):.6}')
                print(f'corpus Mscore = {np.mean(Mscore):.6}')
                print(f'corpus Gscore = {np.mean(Gscore):.6}')
                print(f'corpus CEscore = {np.mean(CEscore):.6}')
           
                for SS, MS, GS, CES in zip(Sscore,Mscore, Gscore, CEscore):
                    results.append(f"{SS:9.6}  ;  {MS:9.6}  ;  {GS:9.6}  ;  {CES:9.6} \n")
                with open(args.outs,'w') as outFile:
                    outFile.writelines("  S_score  ;    M_score  ;   G_score   ;   CE_score \n")
                    outFile.writelines(results)

        else:
            print(f"simplified texts file ({args.cand}) doesn't exist")
            return 1
    
    elif os.path.isfile(args.cand):
        print(f"complex texts file ({args.ref}) doesn't exist")
        return 1

    else:
        comp = args.ref
        simp = args.cand
        SS,MS,GS,CES=CE.CEScore(comp,simp)

        if args.s_score_only:
            print(f'Sscore = {SS:.6}')
            
        elif args.m_score_only:
            print(f'Mscore = {MS:.6}')

        elif args.g_score_only:
            print(f'Gscore = {GS:.6}')

        elif args.ce_score_only:
            print(f'corpus CEscore = {CES:.6}')
        else:
            print(f'Sscore = {SS:.6}')
            print(f'Mscore = {MS:.6}')
            print(f'Gscore = {GS:.6}')
            print(f'CEscore = {CES:.6}')
  
  

if __name__ == "__main__":
    main()
