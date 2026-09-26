; benchmark generated from python API
(set-info :status unknown)
(declare-datatypes ((Fn_46 0)) (((fn_46_0) (fn_46_1) (fn_46_2) (fn_46_3) (fn_46_4))))
(declare-datatypes ((Path_46 0)) (((path_46_0) (path_46_1) (path_46_2) (path_46_3) (path_46_4))))
(declare-fun IsEntry_46 (Fn_46) Bool)
(declare-fun EntryAdmissible_46 (Fn_46) Bool)
(declare-fun PublicOrExternal_46 (Fn_46) Bool)
(declare-fun InitializerSurface_46 (Fn_46) Bool)
(declare-fun NoCallerAuthGuard_46 (Fn_46) Bool)
(declare-fun WritesNonInitState_46 (Fn_46) Bool)
(declare-fun ExactAuthorityPrimitive_46 (Fn_46) Bool)
(declare-fun WritesCallerGuardState_46 (Fn_46) Bool)
(declare-fun AssetExecutionSurface_46 (Fn_46) Bool)
(declare-fun MinOutBoundPresent_46 (Fn_46) Bool)
(declare-fun DeadlineBoundPresent_46 (Fn_46) Bool)
(declare-fun DeadlineExecutionSurface_46 (Fn_46) Bool)
(declare-fun FixedToleranceBoundPresent_46 (Fn_46) Bool)
(declare-fun PriceSourceRead_46 (Fn_46) Bool)
(declare-fun RewardWeightSource_46 (Fn_46) Bool)
(declare-fun ShareRatioSource_46 (Fn_46) Bool)
(declare-fun ExternalValueSource_46 (Fn_46) Bool)
(declare-fun CEIViolation_46 (Fn_46) Bool)
(declare-fun ZeroSupplyBranch_46 (Fn_46) Bool)
(declare-fun RawBalanceOfSelf_46 (Fn_46) Bool)
(declare-fun PathFromTo_46 (Path_46 Fn_46 Fn_46) Bool)
(assert
 (forall ((entry_46 Fn_46) )(let (($x25 (= entry_46 fn_46_4)))
 (let (($x28 (= entry_46 fn_46_1)))
 (let (($x29 (= entry_46 fn_46_0)))
 (or $x29 $x28 (= entry_46 fn_46_2) (= entry_46 fn_46_3) $x25)))))
 )
(assert
 (forall ((carrier_46 Fn_46) )(let (($x25 (= carrier_46 fn_46_4)))
 (let (($x28 (= carrier_46 fn_46_1)))
 (let (($x29 (= carrier_46 fn_46_0)))
 (or $x29 $x28 (= carrier_46 fn_46_2) (= carrier_46 fn_46_3) $x25)))))
 )
(assert
 (forall ((path_46 Path_46) )(let (($x51 (= path_46 path_46_4)))
 (let (($x52 (= path_46 path_46_3)))
 (let (($x53 (= path_46 path_46_2)))
 (let (($x54 (= path_46 path_46_1)))
 (let (($x55 (= path_46 path_46_0)))
 (or $x55 $x54 $x53 $x52 $x51)))))))
 )
(assert
 (IsEntry_46 fn_46_0))
(assert
 (EntryAdmissible_46 fn_46_0))
(assert
 (PublicOrExternal_46 fn_46_0))
(assert
 (InitializerSurface_46 fn_46_0))
(assert
 (NoCallerAuthGuard_46 fn_46_0))
(assert
 (WritesNonInitState_46 fn_46_0))
(assert
 (ExactAuthorityPrimitive_46 fn_46_0))
(assert
 (WritesCallerGuardState_46 fn_46_0))
(assert
 (not (AssetExecutionSurface_46 fn_46_0)))
(assert
 (not (MinOutBoundPresent_46 fn_46_0)))
(assert
 (not (DeadlineBoundPresent_46 fn_46_0)))
(assert
 (not (DeadlineExecutionSurface_46 fn_46_0)))
(assert
 (not (FixedToleranceBoundPresent_46 fn_46_0)))
(assert
 (not (PriceSourceRead_46 fn_46_0)))
(assert
 (not (RewardWeightSource_46 fn_46_0)))
(assert
 (not (ShareRatioSource_46 fn_46_0)))
(assert
 (not (ExternalValueSource_46 fn_46_0)))
(assert
 (not (CEIViolation_46 fn_46_0)))
(assert
 (not (ZeroSupplyBranch_46 fn_46_0)))
(assert
 (not (RawBalanceOfSelf_46 fn_46_0)))
(assert
 (not (IsEntry_46 fn_46_1)))
(assert
 (not (EntryAdmissible_46 fn_46_1)))
(assert
 (not (PublicOrExternal_46 fn_46_1)))
(assert
 (not (InitializerSurface_46 fn_46_1)))
(assert
 (NoCallerAuthGuard_46 fn_46_1))
(assert
 (not (WritesNonInitState_46 fn_46_1)))
(assert
 (not (ExactAuthorityPrimitive_46 fn_46_1)))
(assert
 (not (WritesCallerGuardState_46 fn_46_1)))
(assert
 (not (AssetExecutionSurface_46 fn_46_1)))
(assert
 (not (MinOutBoundPresent_46 fn_46_1)))
(assert
 (not (DeadlineBoundPresent_46 fn_46_1)))
(assert
 (not (DeadlineExecutionSurface_46 fn_46_1)))
(assert
 (not (FixedToleranceBoundPresent_46 fn_46_1)))
(assert
 (not (PriceSourceRead_46 fn_46_1)))
(assert
 (not (RewardWeightSource_46 fn_46_1)))
(assert
 (not (ShareRatioSource_46 fn_46_1)))
(assert
 (not (ExternalValueSource_46 fn_46_1)))
(assert
 (not (CEIViolation_46 fn_46_1)))
(assert
 (not (ZeroSupplyBranch_46 fn_46_1)))
(assert
 (not (RawBalanceOfSelf_46 fn_46_1)))
(assert
 (not (IsEntry_46 fn_46_2)))
(assert
 (not (EntryAdmissible_46 fn_46_2)))
(assert
 (not (PublicOrExternal_46 fn_46_2)))
(assert
 (not (InitializerSurface_46 fn_46_2)))
(assert
 (NoCallerAuthGuard_46 fn_46_2))
(assert
 (WritesNonInitState_46 fn_46_2))
(assert
 (ExactAuthorityPrimitive_46 fn_46_2))
(assert
 (WritesCallerGuardState_46 fn_46_2))
(assert
 (not (AssetExecutionSurface_46 fn_46_2)))
(assert
 (not (MinOutBoundPresent_46 fn_46_2)))
(assert
 (not (DeadlineBoundPresent_46 fn_46_2)))
(assert
 (not (DeadlineExecutionSurface_46 fn_46_2)))
(assert
 (not (FixedToleranceBoundPresent_46 fn_46_2)))
(assert
 (not (PriceSourceRead_46 fn_46_2)))
(assert
 (not (RewardWeightSource_46 fn_46_2)))
(assert
 (not (ShareRatioSource_46 fn_46_2)))
(assert
 (not (ExternalValueSource_46 fn_46_2)))
(assert
 (not (CEIViolation_46 fn_46_2)))
(assert
 (not (ZeroSupplyBranch_46 fn_46_2)))
(assert
 (not (RawBalanceOfSelf_46 fn_46_2)))
(assert
 (not (IsEntry_46 fn_46_3)))
(assert
 (not (EntryAdmissible_46 fn_46_3)))
(assert
 (not (PublicOrExternal_46 fn_46_3)))
(assert
 (not (InitializerSurface_46 fn_46_3)))
(assert
 (NoCallerAuthGuard_46 fn_46_3))
(assert
 (WritesNonInitState_46 fn_46_3))
(assert
 (ExactAuthorityPrimitive_46 fn_46_3))
(assert
 (WritesCallerGuardState_46 fn_46_3))
(assert
 (not (AssetExecutionSurface_46 fn_46_3)))
(assert
 (not (MinOutBoundPresent_46 fn_46_3)))
(assert
 (not (DeadlineBoundPresent_46 fn_46_3)))
(assert
 (not (DeadlineExecutionSurface_46 fn_46_3)))
(assert
 (not (FixedToleranceBoundPresent_46 fn_46_3)))
(assert
 (not (PriceSourceRead_46 fn_46_3)))
(assert
 (not (RewardWeightSource_46 fn_46_3)))
(assert
 (not (ShareRatioSource_46 fn_46_3)))
(assert
 (not (ExternalValueSource_46 fn_46_3)))
(assert
 (not (CEIViolation_46 fn_46_3)))
(assert
 (not (ZeroSupplyBranch_46 fn_46_3)))
(assert
 (not (RawBalanceOfSelf_46 fn_46_3)))
(assert
 (not (IsEntry_46 fn_46_4)))
(assert
 (not (EntryAdmissible_46 fn_46_4)))
(assert
 (PublicOrExternal_46 fn_46_4))
(assert
 (not (InitializerSurface_46 fn_46_4)))
(assert
 (NoCallerAuthGuard_46 fn_46_4))
(assert
 (not (WritesNonInitState_46 fn_46_4)))
(assert
 (not (ExactAuthorityPrimitive_46 fn_46_4)))
(assert
 (not (WritesCallerGuardState_46 fn_46_4)))
(assert
 (not (AssetExecutionSurface_46 fn_46_4)))
(assert
 (not (MinOutBoundPresent_46 fn_46_4)))
(assert
 (not (DeadlineBoundPresent_46 fn_46_4)))
(assert
 (not (DeadlineExecutionSurface_46 fn_46_4)))
(assert
 (not (FixedToleranceBoundPresent_46 fn_46_4)))
(assert
 (not (PriceSourceRead_46 fn_46_4)))
(assert
 (not (RewardWeightSource_46 fn_46_4)))
(assert
 (not (ShareRatioSource_46 fn_46_4)))
(assert
 (not (ExternalValueSource_46 fn_46_4)))
(assert
 (not (CEIViolation_46 fn_46_4)))
(assert
 (not (ZeroSupplyBranch_46 fn_46_4)))
(assert
 (not (RawBalanceOfSelf_46 fn_46_4)))
(assert
 (PathFromTo_46 path_46_0 fn_46_0 fn_46_0))
(assert
 (PathFromTo_46 path_46_1 fn_46_0 fn_46_1))
(assert
 (PathFromTo_46 path_46_2 fn_46_0 fn_46_2))
(assert
 (PathFromTo_46 path_46_3 fn_46_0 fn_46_3))
(assert
 (PathFromTo_46 path_46_4 fn_46_0 fn_46_4))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_0 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_0 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_0 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_0 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_1 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_1 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_1 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_1 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_1 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_2 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_2 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_2 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_2 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_2 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_3 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_3 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_3 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_3 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_3 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_4 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_4 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_4 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_4 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_0 fn_46_4 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_0 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_0 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_0 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_0 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_1 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_1 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_1 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_1 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_1 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_2 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_2 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_2 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_2 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_2 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_3 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_3 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_3 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_3 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_3 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_4 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_4 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_4 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_4 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_1 fn_46_4 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_0 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_0 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_0 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_0 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_1 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_1 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_1 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_1 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_1 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_2 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_2 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_2 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_2 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_2 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_3 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_3 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_3 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_3 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_3 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_4 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_4 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_4 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_4 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_2 fn_46_4 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_0 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_0 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_0 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_0 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_1 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_1 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_1 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_1 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_1 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_2 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_2 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_2 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_2 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_2 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_3 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_3 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_3 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_3 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_3 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_4 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_4 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_4 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_4 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_3 fn_46_4 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_0 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_0 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_0 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_0 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_1 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_1 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_1 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_1 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_1 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_2 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_2 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_2 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_2 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_2 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_3 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_3 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_3 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_3 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_3 fn_46_4)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_4 fn_46_0)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_4 fn_46_1)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_4 fn_46_2)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_4 fn_46_3)))
(assert
 (not (PathFromTo_46 path_46_4 fn_46_4 fn_46_4)))
(assert
 (exists ((w_entry_46 Fn_46) (w_carrier_46 Fn_46) (w_path_46 Path_46) )(and (IsEntry_46 w_entry_46) (EntryAdmissible_46 w_entry_46) (PublicOrExternal_46 w_entry_46) (NoCallerAuthGuard_46 w_entry_46) (PathFromTo_46 w_path_46 w_entry_46 w_carrier_46) (WritesNonInitState_46 w_carrier_46) (or (ExactAuthorityPrimitive_46 w_carrier_46) (WritesCallerGuardState_46 w_carrier_46)) (InitializerSurface_46 w_entry_46)))
)
(check-sat)
