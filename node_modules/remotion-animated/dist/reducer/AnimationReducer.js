import reductionStrategyForProperty, { ReductionStrategy, } from './ReductionStrategy';
const reduceComputedValues = (valueLists) => valueLists.reduce((acc, valueList) => {
    const properties = Object.keys(valueList);
    const reducedValues = Object.assign({}, acc);
    properties.forEach((property) => {
        let reducedValue = valueList[property];
        if (acc[property] !== undefined && reducedValue !== undefined) {
            reducedValue = reduceValue(property, reducedValue, acc);
        }
        reducedValues[property] = reducedValue;
    });
    return reducedValues;
}, {});
function reduceValue(property, reducedValue, acc) {
    var _a, _b;
    const strategy = reductionStrategyForProperty(property);
    switch (strategy) {
        case ReductionStrategy.Addition:
            return ((_a = acc[property]) !== null && _a !== void 0 ? _a : 0) + (reducedValue !== null && reducedValue !== void 0 ? reducedValue : 0);
        case ReductionStrategy.Multiplication:
            return ((_b = acc[property]) !== null && _b !== void 0 ? _b : 1) * (reducedValue !== null && reducedValue !== void 0 ? reducedValue : 1);
        case ReductionStrategy.IgnorePreviousValue:
        default:
            return reducedValue;
    }
}
export default reduceComputedValues;
