import transformStyles from './TransformStyles';
const stylesFromValues = (values) => {
    const properties = {};
    const transform = transformStyles(values);
    if (values.opacity !== undefined)
        properties.opacity = values.opacity;
    if (values.width !== undefined)
        properties.width = values.width;
    if (values.height !== undefined)
        properties.height = values.height;
    if (transform)
        properties.transform = transform;
    return properties;
};
export default stylesFromValues;
