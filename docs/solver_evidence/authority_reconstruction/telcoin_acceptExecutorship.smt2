; benchmark generated from python API
(set-info :status unknown)
(declare-datatypes ((Fn_692 0)) (((fn_692_0) (fn_692_1) (fn_692_2) (fn_692_3))))
(declare-datatypes ((Path_692 0)) (((path_692_0) (path_692_1) (path_692_2) (path_692_3))))
(declare-fun IsEntry_692 (Fn_692) Bool)
(declare-fun EntryAdmissible_692 (Fn_692) Bool)
(declare-fun PublicOrExternal_692 (Fn_692) Bool)
(declare-fun InitializerSurface_692 (Fn_692) Bool)
(declare-fun NoCallerAuthGuard_692 (Fn_692) Bool)
(declare-fun WritesNonInitState_692 (Fn_692) Bool)
(declare-fun ExactAuthorityPrimitive_692 (Fn_692) Bool)
(declare-fun WritesCallerGuardState_692 (Fn_692) Bool)
(declare-fun AssetExecutionSurface_692 (Fn_692) Bool)
(declare-fun MinOutBoundPresent_692 (Fn_692) Bool)
(declare-fun DeadlineBoundPresent_692 (Fn_692) Bool)
(declare-fun DeadlineExecutionSurface_692 (Fn_692) Bool)
(declare-fun FixedToleranceBoundPresent_692 (Fn_692) Bool)
(declare-fun PriceSourceRead_692 (Fn_692) Bool)
(declare-fun RewardWeightSource_692 (Fn_692) Bool)
(declare-fun ShareRatioSource_692 (Fn_692) Bool)
(declare-fun ExternalValueSource_692 (Fn_692) Bool)
(declare-fun CEIViolation_692 (Fn_692) Bool)
(declare-fun ZeroSupplyBranch_692 (Fn_692) Bool)
(declare-fun RawBalanceOfSelf_692 (Fn_692) Bool)
(declare-fun PathFromTo_692 (Path_692 Fn_692 Fn_692) Bool)
(assert
 (forall ((entry_692 Fn_692) )(or (= entry_692 fn_692_0) (= entry_692 fn_692_1) (= entry_692 fn_692_2) (= entry_692 fn_692_3)))
 )
(assert
 (forall ((carrier_692 Fn_692) )(or (= carrier_692 fn_692_0) (= carrier_692 fn_692_1) (= carrier_692 fn_692_2) (= carrier_692 fn_692_3)))
 )
(assert
 (forall ((path_692 Path_692) )(or (= path_692 path_692_0) (= path_692 path_692_1) (= path_692 path_692_2) (= path_692 path_692_3)))
 )
(assert
 (IsEntry_692 fn_692_0))
(assert
 (EntryAdmissible_692 fn_692_0))
(assert
 (PublicOrExternal_692 fn_692_0))
(assert
 (not (InitializerSurface_692 fn_692_0)))
(assert
 (not (NoCallerAuthGuard_692 fn_692_0)))
(assert
 (WritesNonInitState_692 fn_692_0))
(assert
 (not (ExactAuthorityPrimitive_692 fn_692_0)))
(assert
 (WritesCallerGuardState_692 fn_692_0))
(assert
 (not (AssetExecutionSurface_692 fn_692_0)))
(assert
 (not (MinOutBoundPresent_692 fn_692_0)))
(assert
 (not (DeadlineBoundPresent_692 fn_692_0)))
(assert
 (not (DeadlineExecutionSurface_692 fn_692_0)))
(assert
 (not (FixedToleranceBoundPresent_692 fn_692_0)))
(assert
 (not (PriceSourceRead_692 fn_692_0)))
(assert
 (not (RewardWeightSource_692 fn_692_0)))
(assert
 (not (ShareRatioSource_692 fn_692_0)))
(assert
 (not (ExternalValueSource_692 fn_692_0)))
(assert
 (not (CEIViolation_692 fn_692_0)))
(assert
 (not (ZeroSupplyBranch_692 fn_692_0)))
(assert
 (not (RawBalanceOfSelf_692 fn_692_0)))
(assert
 (not (IsEntry_692 fn_692_1)))
(assert
 (not (EntryAdmissible_692 fn_692_1)))
(assert
 (not (PublicOrExternal_692 fn_692_1)))
(assert
 (not (InitializerSurface_692 fn_692_1)))
(assert
 (NoCallerAuthGuard_692 fn_692_1))
(assert
 (not (WritesNonInitState_692 fn_692_1)))
(assert
 (not (ExactAuthorityPrimitive_692 fn_692_1)))
(assert
 (not (WritesCallerGuardState_692 fn_692_1)))
(assert
 (not (AssetExecutionSurface_692 fn_692_1)))
(assert
 (not (MinOutBoundPresent_692 fn_692_1)))
(assert
 (not (DeadlineBoundPresent_692 fn_692_1)))
(assert
 (not (DeadlineExecutionSurface_692 fn_692_1)))
(assert
 (not (FixedToleranceBoundPresent_692 fn_692_1)))
(assert
 (not (PriceSourceRead_692 fn_692_1)))
(assert
 (not (RewardWeightSource_692 fn_692_1)))
(assert
 (not (ShareRatioSource_692 fn_692_1)))
(assert
 (not (ExternalValueSource_692 fn_692_1)))
(assert
 (not (CEIViolation_692 fn_692_1)))
(assert
 (not (ZeroSupplyBranch_692 fn_692_1)))
(assert
 (not (RawBalanceOfSelf_692 fn_692_1)))
(assert
 (not (IsEntry_692 fn_692_2)))
(assert
 (not (EntryAdmissible_692 fn_692_2)))
(assert
 (PublicOrExternal_692 fn_692_2))
(assert
 (not (InitializerSurface_692 fn_692_2)))
(assert
 (NoCallerAuthGuard_692 fn_692_2))
(assert
 (not (WritesNonInitState_692 fn_692_2)))
(assert
 (not (ExactAuthorityPrimitive_692 fn_692_2)))
(assert
 (not (WritesCallerGuardState_692 fn_692_2)))
(assert
 (not (AssetExecutionSurface_692 fn_692_2)))
(assert
 (not (MinOutBoundPresent_692 fn_692_2)))
(assert
 (not (DeadlineBoundPresent_692 fn_692_2)))
(assert
 (not (DeadlineExecutionSurface_692 fn_692_2)))
(assert
 (not (FixedToleranceBoundPresent_692 fn_692_2)))
(assert
 (not (PriceSourceRead_692 fn_692_2)))
(assert
 (not (RewardWeightSource_692 fn_692_2)))
(assert
 (not (ShareRatioSource_692 fn_692_2)))
(assert
 (not (ExternalValueSource_692 fn_692_2)))
(assert
 (not (CEIViolation_692 fn_692_2)))
(assert
 (not (ZeroSupplyBranch_692 fn_692_2)))
(assert
 (not (RawBalanceOfSelf_692 fn_692_2)))
(assert
 (not (IsEntry_692 fn_692_3)))
(assert
 (not (EntryAdmissible_692 fn_692_3)))
(assert
 (PublicOrExternal_692 fn_692_3))
(assert
 (not (InitializerSurface_692 fn_692_3)))
(assert
 (NoCallerAuthGuard_692 fn_692_3))
(assert
 (not (WritesNonInitState_692 fn_692_3)))
(assert
 (not (ExactAuthorityPrimitive_692 fn_692_3)))
(assert
 (not (WritesCallerGuardState_692 fn_692_3)))
(assert
 (not (AssetExecutionSurface_692 fn_692_3)))
(assert
 (not (MinOutBoundPresent_692 fn_692_3)))
(assert
 (not (DeadlineBoundPresent_692 fn_692_3)))
(assert
 (not (DeadlineExecutionSurface_692 fn_692_3)))
(assert
 (not (FixedToleranceBoundPresent_692 fn_692_3)))
(assert
 (not (PriceSourceRead_692 fn_692_3)))
(assert
 (not (RewardWeightSource_692 fn_692_3)))
(assert
 (not (ShareRatioSource_692 fn_692_3)))
(assert
 (not (ExternalValueSource_692 fn_692_3)))
(assert
 (not (CEIViolation_692 fn_692_3)))
(assert
 (not (ZeroSupplyBranch_692 fn_692_3)))
(assert
 (not (RawBalanceOfSelf_692 fn_692_3)))
(assert
 (PathFromTo_692 path_692_0 fn_692_0 fn_692_0))
(assert
 (PathFromTo_692 path_692_1 fn_692_0 fn_692_1))
(assert
 (PathFromTo_692 path_692_2 fn_692_0 fn_692_2))
(assert
 (PathFromTo_692 path_692_3 fn_692_0 fn_692_3))
(assert
 (not (PathFromTo_692 path_692_0 fn_692_0 fn_692_1)))
(assert
 (not (PathFromTo_692 path_692_0 fn_692_0 fn_692_2)))
(assert
 (not (PathFromTo_692 path_692_0 fn_692_0 fn_692_3)))
(assert
 (not (PathFromTo_692 path_692_0 fn_692_1 fn_692_0)))
(assert
 (not (PathFromTo_692 path_692_0 fn_692_1 fn_692_1)))
(assert
 (not (PathFromTo_692 path_692_0 fn_692_1 fn_692_2)))
(assert
 (not (PathFromTo_692 path_692_0 fn_692_1 fn_692_3)))
(assert
 (not (PathFromTo_692 path_692_0 fn_692_2 fn_692_0)))
(assert
 (not (PathFromTo_692 path_692_0 fn_692_2 fn_692_1)))
(assert
 (not (PathFromTo_692 path_692_0 fn_692_2 fn_692_2)))
(assert
 (not (PathFromTo_692 path_692_0 fn_692_2 fn_692_3)))
(assert
 (not (PathFromTo_692 path_692_0 fn_692_3 fn_692_0)))
(assert
 (not (PathFromTo_692 path_692_0 fn_692_3 fn_692_1)))
(assert
 (not (PathFromTo_692 path_692_0 fn_692_3 fn_692_2)))
(assert
 (not (PathFromTo_692 path_692_0 fn_692_3 fn_692_3)))
(assert
 (not (PathFromTo_692 path_692_1 fn_692_0 fn_692_0)))
(assert
 (not (PathFromTo_692 path_692_1 fn_692_0 fn_692_2)))
(assert
 (not (PathFromTo_692 path_692_1 fn_692_0 fn_692_3)))
(assert
 (not (PathFromTo_692 path_692_1 fn_692_1 fn_692_0)))
(assert
 (not (PathFromTo_692 path_692_1 fn_692_1 fn_692_1)))
(assert
 (not (PathFromTo_692 path_692_1 fn_692_1 fn_692_2)))
(assert
 (not (PathFromTo_692 path_692_1 fn_692_1 fn_692_3)))
(assert
 (not (PathFromTo_692 path_692_1 fn_692_2 fn_692_0)))
(assert
 (not (PathFromTo_692 path_692_1 fn_692_2 fn_692_1)))
(assert
 (not (PathFromTo_692 path_692_1 fn_692_2 fn_692_2)))
(assert
 (not (PathFromTo_692 path_692_1 fn_692_2 fn_692_3)))
(assert
 (not (PathFromTo_692 path_692_1 fn_692_3 fn_692_0)))
(assert
 (not (PathFromTo_692 path_692_1 fn_692_3 fn_692_1)))
(assert
 (not (PathFromTo_692 path_692_1 fn_692_3 fn_692_2)))
(assert
 (not (PathFromTo_692 path_692_1 fn_692_3 fn_692_3)))
(assert
 (not (PathFromTo_692 path_692_2 fn_692_0 fn_692_0)))
(assert
 (not (PathFromTo_692 path_692_2 fn_692_0 fn_692_1)))
(assert
 (not (PathFromTo_692 path_692_2 fn_692_0 fn_692_3)))
(assert
 (not (PathFromTo_692 path_692_2 fn_692_1 fn_692_0)))
(assert
 (not (PathFromTo_692 path_692_2 fn_692_1 fn_692_1)))
(assert
 (not (PathFromTo_692 path_692_2 fn_692_1 fn_692_2)))
(assert
 (not (PathFromTo_692 path_692_2 fn_692_1 fn_692_3)))
(assert
 (not (PathFromTo_692 path_692_2 fn_692_2 fn_692_0)))
(assert
 (not (PathFromTo_692 path_692_2 fn_692_2 fn_692_1)))
(assert
 (not (PathFromTo_692 path_692_2 fn_692_2 fn_692_2)))
(assert
 (not (PathFromTo_692 path_692_2 fn_692_2 fn_692_3)))
(assert
 (not (PathFromTo_692 path_692_2 fn_692_3 fn_692_0)))
(assert
 (not (PathFromTo_692 path_692_2 fn_692_3 fn_692_1)))
(assert
 (not (PathFromTo_692 path_692_2 fn_692_3 fn_692_2)))
(assert
 (not (PathFromTo_692 path_692_2 fn_692_3 fn_692_3)))
(assert
 (not (PathFromTo_692 path_692_3 fn_692_0 fn_692_0)))
(assert
 (not (PathFromTo_692 path_692_3 fn_692_0 fn_692_1)))
(assert
 (not (PathFromTo_692 path_692_3 fn_692_0 fn_692_2)))
(assert
 (not (PathFromTo_692 path_692_3 fn_692_1 fn_692_0)))
(assert
 (not (PathFromTo_692 path_692_3 fn_692_1 fn_692_1)))
(assert
 (not (PathFromTo_692 path_692_3 fn_692_1 fn_692_2)))
(assert
 (not (PathFromTo_692 path_692_3 fn_692_1 fn_692_3)))
(assert
 (not (PathFromTo_692 path_692_3 fn_692_2 fn_692_0)))
(assert
 (not (PathFromTo_692 path_692_3 fn_692_2 fn_692_1)))
(assert
 (not (PathFromTo_692 path_692_3 fn_692_2 fn_692_2)))
(assert
 (not (PathFromTo_692 path_692_3 fn_692_2 fn_692_3)))
(assert
 (not (PathFromTo_692 path_692_3 fn_692_3 fn_692_0)))
(assert
 (not (PathFromTo_692 path_692_3 fn_692_3 fn_692_1)))
(assert
 (not (PathFromTo_692 path_692_3 fn_692_3 fn_692_2)))
(assert
 (not (PathFromTo_692 path_692_3 fn_692_3 fn_692_3)))
(assert
 (exists ((w_entry_692 Fn_692) (w_carrier_692 Fn_692) (w_path_692 Path_692) )(and (IsEntry_692 w_entry_692) (EntryAdmissible_692 w_entry_692) (PublicOrExternal_692 w_entry_692) (NoCallerAuthGuard_692 w_entry_692) (PathFromTo_692 w_path_692 w_entry_692 w_carrier_692) (WritesNonInitState_692 w_carrier_692) (or (ExactAuthorityPrimitive_692 w_carrier_692) (WritesCallerGuardState_692 w_carrier_692)) (not (InitializerSurface_692 w_entry_692))))
)
(check-sat)
