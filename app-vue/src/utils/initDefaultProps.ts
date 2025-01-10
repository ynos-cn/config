/*
 * @Description: 
 * @Version: 1.0
 * @Autor: jiajun.wu
 * @Date: 2022-08-26 14:10:28
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2023-01-04 16:57:54
 */
import type { ExtractPropTypes, PropType } from 'vue';
import type { VueTypeValidableDef, VueTypeDef } from 'vue-types';

export const initDefaultProps = <T>(
  types: T,
  defaultProps: {
    [K in keyof T]?: T[K] extends VueTypeValidableDef<infer U>
    ? U
    : T[K] extends VueTypeDef<infer U>
    ? U
    : T[K] extends { type: PropType<infer U> }
    ? U
    : any;
  },
): T => {

  const propTypes: T = { ...types };
  Object.keys(defaultProps).forEach(k => {
    const prop = propTypes[k] as VueTypeValidableDef;
    if (prop) {
      if (prop.type || prop.default) {
        prop.default = defaultProps[k];
      } else if (prop.def) {
        prop.def(defaultProps[k]);
      } else {
        propTypes[k] = { type: prop, default: defaultProps[k] };
      }
    } else {
      throw new Error(`not have ${k} prop`);
    }
  });
  return propTypes;
};


export const handlerProps = <T>(
  types: T,
  props: {
    [K in keyof T]?: T[K] extends VueTypeValidableDef<infer U>
    ? U
    : T[K] extends VueTypeDef<infer U>
    ? U
    : T[K] extends { type: PropType<infer U> }
    ? U
    : any;
  }
): Partial<ExtractPropTypes<T>> => {
  const propTypes = {};
  Object.keys(props).map(k => {
    const prop = types[k] as VueTypeValidableDef;
    if (prop) {
      propTypes[k] = props[k]
    }
  })
  return propTypes;
}