export var ReductionStrategy;
(function (ReductionStrategy) {
    ReductionStrategy[ReductionStrategy["Addition"] = 0] = "Addition";
    ReductionStrategy[ReductionStrategy["Multiplication"] = 1] = "Multiplication";
    ReductionStrategy[ReductionStrategy["IgnorePreviousValue"] = 2] = "IgnorePreviousValue";
})(ReductionStrategy || (ReductionStrategy = {}));
const reductionStrategyForProperty = (property) => {
    switch (property) {
        case 'translateX':
        case 'translateY':
        case 'translateZ':
        case 'rotateX':
        case 'rotateY':
        case 'rotateZ':
            return ReductionStrategy.Addition;
        case 'scaleX':
        case 'scaleY':
        case 'scaleZ':
            return ReductionStrategy.Multiplication;
        case 'opacity':
        case 'width':
        case 'height':
        default:
            return ReductionStrategy.IgnorePreviousValue;
    }
};
export default reductionStrategyForProperty;
