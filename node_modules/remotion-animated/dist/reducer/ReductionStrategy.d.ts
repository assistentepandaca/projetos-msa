import AnimationValues from './AnimationValues';
export declare enum ReductionStrategy {
    Addition = 0,
    Multiplication = 1,
    IgnorePreviousValue = 2
}
declare const reductionStrategyForProperty: (property: keyof AnimationValues) => ReductionStrategy;
export default reductionStrategyForProperty;
//# sourceMappingURL=ReductionStrategy.d.ts.map