************************************************************************
      FUNCTION BendFactor(Q2,A0_DIS,B0_DIS,C0_DIS)
************************************************************************
*                                                                      *
*                                                                      *
************************************************************************

         USE PhysMathConstants, ONLY: one

         IMPLICIT REAL*8 (A-M,O-Z), INTEGER (N)

         COMMON   /n_BF_DIS/n_BF_DIS                                     Switch for type of "bend-factor" for DIS structure functions

         SELECTCASE(n_BF_DIS)
               CASE(       1)
               BendFactor= one
               CASE(       2)
               BendFactor= Q2/(Q2+A0_DIS)                                One parameter "bend-factor"
               CASE(       4)
               BendFactor= Q2/(Q2+A0_DIS)+B0_DIS*C0_DIS/(Q2+C0_DIS)      Four parameter "bend-factor"
      endSELECT

         RETURN
      END FUNCTION BendFactor
