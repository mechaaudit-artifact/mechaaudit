; benchmark generated from python API
(set-info :status unknown)
(declare-datatypes ((Fn_5 0)) (((fn_5_0) (fn_5_1) (fn_5_2) (fn_5_3) (fn_5_4) (fn_5_5))))
(declare-datatypes ((Path_5 0)) (((path_5_0) (path_5_1) (path_5_2) (path_5_3) (path_5_4) (path_5_5))))
(declare-fun IsEntry_5 (Fn_5) Bool)
(declare-fun EntryAdmissible_5 (Fn_5) Bool)
(declare-fun PublicOrExternal_5 (Fn_5) Bool)
(declare-fun InitializerSurface_5 (Fn_5) Bool)
(declare-fun NoCallerAuthGuard_5 (Fn_5) Bool)
(declare-fun WritesNonInitState_5 (Fn_5) Bool)
(declare-fun ExactAuthorityPrimitive_5 (Fn_5) Bool)
(declare-fun WritesCallerGuardState_5 (Fn_5) Bool)
(declare-fun AssetExecutionSurface_5 (Fn_5) Bool)
(declare-fun MinOutBoundPresent_5 (Fn_5) Bool)
(declare-fun DeadlineBoundPresent_5 (Fn_5) Bool)
(declare-fun DeadlineExecutionSurface_5 (Fn_5) Bool)
(declare-fun FixedToleranceBoundPresent_5 (Fn_5) Bool)
(declare-fun PriceSourceRead_5 (Fn_5) Bool)
(declare-fun RewardWeightSource_5 (Fn_5) Bool)
(declare-fun ShareRatioSource_5 (Fn_5) Bool)
(declare-fun ExternalValueSource_5 (Fn_5) Bool)
(declare-fun CEIViolation_5 (Fn_5) Bool)
(declare-fun ZeroSupplyBranch_5 (Fn_5) Bool)
(declare-fun RawBalanceOfSelf_5 (Fn_5) Bool)
(declare-fun PathFromTo_5 (Path_5 Fn_5 Fn_5) Bool)
(assert
 (forall ((entry_5 Fn_5) )(let (($x28 (= entry_5 fn_5_5)))
 (let (($x29 (= entry_5 fn_5_4)))
 (let (($x30 (= entry_5 fn_5_3)))
 (let (($x31 (= entry_5 fn_5_2)))
 (let (($x32 (= entry_5 fn_5_1)))
 (let (($x33 (= entry_5 fn_5_0)))
 (or $x33 $x32 $x31 $x30 $x29 $x28))))))))
 )
(assert
 (forall ((carrier_5 Fn_5) )(let (($x28 (= carrier_5 fn_5_5)))
 (let (($x29 (= carrier_5 fn_5_4)))
 (let (($x30 (= carrier_5 fn_5_3)))
 (let (($x31 (= carrier_5 fn_5_2)))
 (let (($x32 (= carrier_5 fn_5_1)))
 (let (($x33 (= carrier_5 fn_5_0)))
 (or $x33 $x32 $x31 $x30 $x29 $x28))))))))
 )
(assert
 (forall ((path_5 Path_5) )(let (($x55 (= path_5 path_5_5)))
 (let (($x56 (= path_5 path_5_4)))
 (let (($x57 (= path_5 path_5_3)))
 (let (($x58 (= path_5 path_5_2)))
 (let (($x59 (= path_5 path_5_1)))
 (let (($x60 (= path_5 path_5_0)))
 (or $x60 $x59 $x58 $x57 $x56 $x55))))))))
 )
(assert
 (IsEntry_5 fn_5_0))
(assert
 (EntryAdmissible_5 fn_5_0))
(assert
 (PublicOrExternal_5 fn_5_0))
(assert
 (not (InitializerSurface_5 fn_5_0)))
(assert
 (NoCallerAuthGuard_5 fn_5_0))
(assert
 (not (WritesNonInitState_5 fn_5_0)))
(assert
 (not (ExactAuthorityPrimitive_5 fn_5_0)))
(assert
 (not (WritesCallerGuardState_5 fn_5_0)))
(assert
 (not (AssetExecutionSurface_5 fn_5_0)))
(assert
 (not (MinOutBoundPresent_5 fn_5_0)))
(assert
 (not (DeadlineBoundPresent_5 fn_5_0)))
(assert
 (not (DeadlineExecutionSurface_5 fn_5_0)))
(assert
 (not (FixedToleranceBoundPresent_5 fn_5_0)))
(assert
 (not (PriceSourceRead_5 fn_5_0)))
(assert
 (not (RewardWeightSource_5 fn_5_0)))
(assert
 (not (ShareRatioSource_5 fn_5_0)))
(assert
 (not (ExternalValueSource_5 fn_5_0)))
(assert
 (not (CEIViolation_5 fn_5_0)))
(assert
 (ZeroSupplyBranch_5 fn_5_0))
(assert
 (not (RawBalanceOfSelf_5 fn_5_0)))
(assert
 (not (IsEntry_5 fn_5_1)))
(assert
 (not (EntryAdmissible_5 fn_5_1)))
(assert
 (PublicOrExternal_5 fn_5_1))
(assert
 (not (InitializerSurface_5 fn_5_1)))
(assert
 (NoCallerAuthGuard_5 fn_5_1))
(assert
 (not (WritesNonInitState_5 fn_5_1)))
(assert
 (not (ExactAuthorityPrimitive_5 fn_5_1)))
(assert
 (not (WritesCallerGuardState_5 fn_5_1)))
(assert
 (not (AssetExecutionSurface_5 fn_5_1)))
(assert
 (not (MinOutBoundPresent_5 fn_5_1)))
(assert
 (not (DeadlineBoundPresent_5 fn_5_1)))
(assert
 (not (DeadlineExecutionSurface_5 fn_5_1)))
(assert
 (not (FixedToleranceBoundPresent_5 fn_5_1)))
(assert
 (not (PriceSourceRead_5 fn_5_1)))
(assert
 (not (RewardWeightSource_5 fn_5_1)))
(assert
 (not (ShareRatioSource_5 fn_5_1)))
(assert
 (not (ExternalValueSource_5 fn_5_1)))
(assert
 (not (CEIViolation_5 fn_5_1)))
(assert
 (ZeroSupplyBranch_5 fn_5_1))
(assert
 (RawBalanceOfSelf_5 fn_5_1))
(assert
 (not (IsEntry_5 fn_5_2)))
(assert
 (not (EntryAdmissible_5 fn_5_2)))
(assert
 (not (PublicOrExternal_5 fn_5_2)))
(assert
 (not (InitializerSurface_5 fn_5_2)))
(assert
 (NoCallerAuthGuard_5 fn_5_2))
(assert
 (not (WritesNonInitState_5 fn_5_2)))
(assert
 (not (ExactAuthorityPrimitive_5 fn_5_2)))
(assert
 (not (WritesCallerGuardState_5 fn_5_2)))
(assert
 (not (AssetExecutionSurface_5 fn_5_2)))
(assert
 (not (MinOutBoundPresent_5 fn_5_2)))
(assert
 (not (DeadlineBoundPresent_5 fn_5_2)))
(assert
 (not (DeadlineExecutionSurface_5 fn_5_2)))
(assert
 (not (FixedToleranceBoundPresent_5 fn_5_2)))
(assert
 (not (PriceSourceRead_5 fn_5_2)))
(assert
 (not (RewardWeightSource_5 fn_5_2)))
(assert
 (not (ShareRatioSource_5 fn_5_2)))
(assert
 (not (ExternalValueSource_5 fn_5_2)))
(assert
 (not (CEIViolation_5 fn_5_2)))
(assert
 (not (ZeroSupplyBranch_5 fn_5_2)))
(assert
 (not (RawBalanceOfSelf_5 fn_5_2)))
(assert
 (not (IsEntry_5 fn_5_3)))
(assert
 (not (EntryAdmissible_5 fn_5_3)))
(assert
 (not (PublicOrExternal_5 fn_5_3)))
(assert
 (not (InitializerSurface_5 fn_5_3)))
(assert
 (NoCallerAuthGuard_5 fn_5_3))
(assert
 (not (WritesNonInitState_5 fn_5_3)))
(assert
 (not (ExactAuthorityPrimitive_5 fn_5_3)))
(assert
 (not (WritesCallerGuardState_5 fn_5_3)))
(assert
 (not (AssetExecutionSurface_5 fn_5_3)))
(assert
 (not (MinOutBoundPresent_5 fn_5_3)))
(assert
 (not (DeadlineBoundPresent_5 fn_5_3)))
(assert
 (not (DeadlineExecutionSurface_5 fn_5_3)))
(assert
 (not (FixedToleranceBoundPresent_5 fn_5_3)))
(assert
 (not (PriceSourceRead_5 fn_5_3)))
(assert
 (not (RewardWeightSource_5 fn_5_3)))
(assert
 (not (ShareRatioSource_5 fn_5_3)))
(assert
 (not (ExternalValueSource_5 fn_5_3)))
(assert
 (not (CEIViolation_5 fn_5_3)))
(assert
 (not (ZeroSupplyBranch_5 fn_5_3)))
(assert
 (not (RawBalanceOfSelf_5 fn_5_3)))
(assert
 (not (IsEntry_5 fn_5_4)))
(assert
 (not (EntryAdmissible_5 fn_5_4)))
(assert
 (PublicOrExternal_5 fn_5_4))
(assert
 (not (InitializerSurface_5 fn_5_4)))
(assert
 (NoCallerAuthGuard_5 fn_5_4))
(assert
 (not (WritesNonInitState_5 fn_5_4)))
(assert
 (not (ExactAuthorityPrimitive_5 fn_5_4)))
(assert
 (not (WritesCallerGuardState_5 fn_5_4)))
(assert
 (not (AssetExecutionSurface_5 fn_5_4)))
(assert
 (not (MinOutBoundPresent_5 fn_5_4)))
(assert
 (not (DeadlineBoundPresent_5 fn_5_4)))
(assert
 (not (DeadlineExecutionSurface_5 fn_5_4)))
(assert
 (not (FixedToleranceBoundPresent_5 fn_5_4)))
(assert
 (not (PriceSourceRead_5 fn_5_4)))
(assert
 (not (RewardWeightSource_5 fn_5_4)))
(assert
 (not (ShareRatioSource_5 fn_5_4)))
(assert
 (not (ExternalValueSource_5 fn_5_4)))
(assert
 (not (CEIViolation_5 fn_5_4)))
(assert
 (not (ZeroSupplyBranch_5 fn_5_4)))
(assert
 (RawBalanceOfSelf_5 fn_5_4))
(assert
 (not (IsEntry_5 fn_5_5)))
(assert
 (not (EntryAdmissible_5 fn_5_5)))
(assert
 (not (PublicOrExternal_5 fn_5_5)))
(assert
 (not (InitializerSurface_5 fn_5_5)))
(assert
 (NoCallerAuthGuard_5 fn_5_5))
(assert
 (not (WritesNonInitState_5 fn_5_5)))
(assert
 (not (ExactAuthorityPrimitive_5 fn_5_5)))
(assert
 (not (WritesCallerGuardState_5 fn_5_5)))
(assert
 (not (AssetExecutionSurface_5 fn_5_5)))
(assert
 (not (MinOutBoundPresent_5 fn_5_5)))
(assert
 (not (DeadlineBoundPresent_5 fn_5_5)))
(assert
 (not (DeadlineExecutionSurface_5 fn_5_5)))
(assert
 (not (FixedToleranceBoundPresent_5 fn_5_5)))
(assert
 (not (PriceSourceRead_5 fn_5_5)))
(assert
 (not (RewardWeightSource_5 fn_5_5)))
(assert
 (not (ShareRatioSource_5 fn_5_5)))
(assert
 (not (ExternalValueSource_5 fn_5_5)))
(assert
 (not (CEIViolation_5 fn_5_5)))
(assert
 (not (ZeroSupplyBranch_5 fn_5_5)))
(assert
 (RawBalanceOfSelf_5 fn_5_5))
(assert
 (PathFromTo_5 path_5_0 fn_5_0 fn_5_0))
(assert
 (PathFromTo_5 path_5_1 fn_5_0 fn_5_1))
(assert
 (PathFromTo_5 path_5_2 fn_5_0 fn_5_2))
(assert
 (PathFromTo_5 path_5_3 fn_5_0 fn_5_3))
(assert
 (PathFromTo_5 path_5_4 fn_5_0 fn_5_4))
(assert
 (PathFromTo_5 path_5_5 fn_5_0 fn_5_5))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_0 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_0 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_0 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_0 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_0 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_1 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_1 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_1 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_1 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_1 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_1 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_2 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_2 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_2 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_2 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_2 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_2 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_3 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_3 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_3 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_3 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_3 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_3 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_4 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_4 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_4 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_4 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_4 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_4 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_5 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_5 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_5 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_5 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_5 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_0 fn_5_5 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_0 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_0 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_0 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_0 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_0 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_1 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_1 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_1 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_1 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_1 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_1 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_2 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_2 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_2 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_2 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_2 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_2 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_3 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_3 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_3 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_3 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_3 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_3 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_4 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_4 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_4 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_4 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_4 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_4 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_5 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_5 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_5 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_5 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_5 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_1 fn_5_5 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_0 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_0 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_0 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_0 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_0 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_1 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_1 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_1 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_1 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_1 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_1 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_2 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_2 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_2 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_2 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_2 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_2 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_3 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_3 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_3 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_3 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_3 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_3 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_4 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_4 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_4 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_4 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_4 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_4 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_5 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_5 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_5 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_5 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_5 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_2 fn_5_5 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_0 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_0 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_0 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_0 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_0 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_1 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_1 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_1 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_1 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_1 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_1 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_2 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_2 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_2 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_2 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_2 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_2 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_3 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_3 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_3 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_3 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_3 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_3 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_4 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_4 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_4 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_4 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_4 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_4 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_5 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_5 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_5 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_5 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_5 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_3 fn_5_5 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_0 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_0 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_0 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_0 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_0 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_1 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_1 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_1 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_1 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_1 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_1 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_2 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_2 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_2 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_2 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_2 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_2 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_3 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_3 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_3 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_3 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_3 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_3 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_4 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_4 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_4 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_4 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_4 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_4 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_5 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_5 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_5 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_5 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_5 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_4 fn_5_5 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_0 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_0 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_0 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_0 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_0 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_1 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_1 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_1 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_1 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_1 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_1 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_2 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_2 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_2 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_2 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_2 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_2 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_3 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_3 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_3 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_3 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_3 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_3 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_4 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_4 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_4 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_4 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_4 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_4 fn_5_5)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_5 fn_5_0)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_5 fn_5_1)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_5 fn_5_2)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_5 fn_5_3)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_5 fn_5_4)))
(assert
 (not (PathFromTo_5 path_5_5 fn_5_5 fn_5_5)))
(assert
 (exists ((w_entry_5 Fn_5) (w_carrier_5 Fn_5) (w_path_5 Path_5) )(and (IsEntry_5 w_entry_5) (EntryAdmissible_5 w_entry_5) (PublicOrExternal_5 w_entry_5) (PathFromTo_5 w_path_5 w_entry_5 w_carrier_5) (ZeroSupplyBranch_5 w_carrier_5) (RawBalanceOfSelf_5 w_carrier_5)))
)
(check-sat)
