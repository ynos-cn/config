/*
 * @Description: 下拉选中组件
 * @Version: 1.0
 * @Autor: jiajun.wu
 * @Date: 2022-08-10 16:47:58
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2023-08-04 14:20:05
 */

import { defineComponent, h, ref, watch, PropType, Ref,useSlots } from 'vue'
import { Select, SelectOption } from 'ant-design-vue'
import { DefaultOptionType, selectProps, SelectValue } from 'ant-design-vue/lib/select'
import less from './index.module.less'
import { axios } from '@/utils/request'
import { ResDataStruct } from '@/interface/base'

const ZSelect = defineComponent({
  name: 'ZSelect',
  props: {
    ...selectProps(),
    findUrl: {
      type: String,
    },
    /** 需要绑定的 值  */
    bingLabel: {
      type: String,
      default: 'name'
    },
    /** 需要绑定的 键  */
    bingValue: {
      type: String,
      default: '_id'
    },
    /** 查询大小 */
    findPageSize: {
      type: Number,
      default: 10
    },
    /** 数据相应的路径 */
    dataPath: {
      type: String,
      default: 'body'
    },
    /** 条件查询 */
    paramBodyData: {
      type: Object,
      default: () => { }
    },
    /** 绑定值查询类型 String Array */
    bingValueFindType: {
      type: String as PropType<'string' | 'array'>,
      default: () => 'string'
    },
    /** 追加选项 */
    pushOptions: {
      type: Array as PropType<Array<DefaultOptionType>>,
      default: () => []
    },
    unshiftOptions: {
      type: Array as PropType<Array<DefaultOptionType>>,
      default: () => []
    },
    /** 接口上下文 */
    apiCtx: {
      type: String,
      default: ''
    },
    /** 展示多个标题 */
    multipleLabel: {
      type: Boolean,
      default: () => false
    },
    /** 需要绑定多个标题的 值  */
    bingMultipleLabel: {
      type: String,
      default: 'title'
    },
    onChangeRecord:Function as PropType<<T extends DefaultOptionType>(value:T) => void>,
    onSelectRecord:Function as PropType<<T extends DefaultOptionType>(value:T) => void>,
    /** 禁用的选项 */
    disabledKeys:{
      type:Array as PropType<Array<string>>,
      default:()=>[]
    }
  },
  setup(props) {
    const eValue: Ref<any> = ref(props.value)
    const options = ref<Array<DefaultOptionType>>(props.options ?? [])
    const initOptionsList = ref<Array<DefaultOptionType>>([])
    const currentPage = ref(1)
    const total = ref(0)
    /** 初始化总数 */
    const initTotal = ref(0)
    const eSearchValue = ref('')

    const doQuery = (callback?: (e: any) => void) => {
      if(!props.findUrl) {
        return
      }
      const setListDataFn = (res:ResDataStruct<any>)=>{
        if (res.success) {
          total.value = res.total ?? 0;
          if (!eSearchValue.value.trim()) {
            initTotal.value = res.total ?? 0;
          }
          let dataPath = props.dataPath.split('.')
          let array = JSON.parse(JSON.stringify(res))
          let bArr: any[] = []
          dataPath.map(v => {
            array = array[v]
          })
          if (!array) {
            return false
          }
          array.map((v: any) => {
            let index = options.value.findIndex(e => e.value == v[props.bingValue])
            if (index <= -1) {
              let dataValue = v.value
              Object.assign(v, {
                dataValue,
                value: v[props.bingValue],
                label: v[props.bingLabel],
                disabled: props.disabledKeys.includes(v[props.bingValue])
              })
              // 如果存在多个标题展示属性，塞入菜单数据中
              if (props.multipleLabel) {
                Object.assign(v, {
                  multipleLabel: v[props.bingMultipleLabel],
                })
              }
              bArr.push(v)
            }
          })
          options.value.push(...bArr)
          initOptionsList.value = JSON.parse(JSON.stringify(options.value))

          if (callback) {
            callback(array)
          }
        }
      }
      axios<ResDataStruct<any>>({
        url: `${props.apiCtx}${props.findUrl}`,
        method: 'post',
        isParallel:true,
        data: {
          body: {
            [`${props.bingLabel}`]: eSearchValue.value.trim() ? eSearchValue.value.trim() : undefined,
            ...props.paramBodyData
          },
          limit: props.findPageSize,
          page: currentPage.value
        }
      }).then(res => {
        setListDataFn(res)
      })
    }
    const handleSelect = (value: SelectValue, _option: DefaultOptionType | DefaultOptionType[]) => {
      let recordData:any = options.value.find(item => item._id == value) //当前选择的数据对象
      if (props.onSelectRecord) {
        /*   如果使用multipleLabel模式，因为是通过 a-select-option children 构造的节点，所以返回的_option是个函数不是选中的数据集合
          所以要从options中去取当前选择的数据对象recordData，用于传递 */
        if (props.multipleLabel) {
          props.onSelectRecord(recordData)
        } else {
          props.onSelectRecord(_option)
        }
      }
    }
    const handleChange = (value: SelectValue, _option: DefaultOptionType | DefaultOptionType[]) => {
      if (!value) {
        eSearchValue.value = ''
        eValue.value = undefined

        if (props.onChangeRecord) {
          props.onChangeRecord(_option)
        }
        if (props.onChange) {
          props.onChange(undefined, _option)
        }
        return false
      }
      let option: Array<DefaultOptionType> = _option as Array<DefaultOptionType>
      if (!Array.isArray(_option)) {
        option = [_option]
      }

      option.map(v => {
        let index = initOptionsList.value.findIndex(e => e?.value == v?.value)
        if (index <= -1) {
          initOptionsList.value.push(v)
        }
      })

      options.value = JSON.parse(JSON.stringify(initOptionsList.value))
      total.value = initTotal.value
      eSearchValue.value = ''
      eValue.value = value

      if (props.onChangeRecord) {
        props.onChangeRecord(_option)
      }
      if (props.onChange) {
        props.onChange(value, _option)
      }
    }

    const doQueryDetails = (_id: SelectValue | Array<SelectValue>) => {
      axios<ResDataStruct>({
        url: `${props.apiCtx}${props.findUrl}`,
        method: "post",
        data: {
          body: {
            [`${props.bingValue}`]: _id
          }
        }
      }).then(res => {
        if (res.success) {
          let dataPath = props.dataPath.split('.')
          let array = JSON.parse(JSON.stringify(res))
          dataPath.map(v => {
            array = array[v]
          })
          if (!array) {
            return false
          }

          array.map((v: any) => {
            let dataValue = v.value
            Object.assign(v, {
              dataValue,
              value: v[props.bingValue],
              label: v[props.bingLabel],
            })
            // 如果存在多个标题展示属性，塞入菜单数据中
            if (props.multipleLabel) {
              Object.assign(v, {
                multipleLabel: v[props.bingMultipleLabel],
              })
            }
            if (options.value.findIndex(e => e.value == v.value) <= -1) {
              options.value.unshift(v)
              initOptionsList.value.unshift(v)
            }
          })
        }
      })
    }

    const handlePopupScroll = (e: any) => {
      const { target } = e
      if (target.scrollTop + target.offsetHeight === target.scrollHeight) {
        if (options.value.length >= total.value) {
          return false
        }
        currentPage.value += 1

        doQuery()
      }

      if(props.onPopupScroll){
        props.onPopupScroll(e)
      }
    }

    let timeout: any;
    let currentValue = '';
    const fetch = (value: string, callback: any) => {
      if (timeout) {
        clearTimeout(timeout);
        timeout = null;
      }
      currentValue = value;
      function fake() {
        axios<ResDataStruct>({
          url: `${props.apiCtx}${props.findUrl}`,
          method: 'post',
          data: {
            body: {
              [`${props.bingLabel}`]: value.trim() ?? undefined,
              ...props.paramBodyData
            },
            limit: props.findPageSize
          }
        }).then(res => {
          if (currentValue === value) {
            if (res.success) {
              total.value = res.total ?? 0;
              eSearchValue.value = value
              let dataPath = props.dataPath.split('.')
              let array = JSON.parse(JSON.stringify(res))
              let bArr: any[] = []
              dataPath.map(v => {
                array = array[v]
              })
              if (!array) {
                return false
              }
              array.map((v: any) => {
                let index = options.value.findIndex(e => e.value == v.value)
                if (index <= -1) {
                  let dataValue = v.value
                  Object.assign(v, {
                    dataValue,
                    value: v[props.bingValue],
                    label: v[props.bingLabel],
                  })
                  // 如果存在多个标题展示属性，塞入菜单数据中
                  if (props.multipleLabel) {
                    Object.assign(v, {
                      multipleLabel: v[props.bingMultipleLabel],
                    })
                  }
                  bArr.push(v)
                }
              })
              if (callback) {
                callback(array, value)
              }
            }
          }
        })
      }

      timeout = setTimeout(fake, 300);
    }

    const handleSearch = (val: string) => {
      if (val.trim()) {
        currentPage.value = 1
        fetch(val, (d: any[], eValue: string) => {
          if (val == eValue) {
            options.value = d
            setPropsOptions()
          } else {
            options.value = JSON.parse(JSON.stringify(initOptionsList.value))
          }
        });
      } else {
        eSearchValue.value = ''
        options.value = JSON.parse(JSON.stringify(initOptionsList.value))
      }

      if (props.onSearch) {
        props.onSearch(val)
      }
    }

    /** 设置默认数据 */
    const setPropsOptions = () => {
      if (props.pushOptions) {
        props.pushOptions.map(v => {
          options.value.push(v)
        })
      }
      if (props.unshiftOptions) {
        props.unshiftOptions.map(v => {
          options.value.unshift(v)
        })
      }
    }

    watch(() => props.findUrl, (val) => {
      if (val && !props.options) {
        doQuery((array: any) => {
          if (props.value) {
            if (Array.isArray(props.value)) {
              let ids: Array<SelectValue> = []
              let recordList: Array<SelectValue> = [] //当前下拉菜单存在的选中数据集合
              props.value.map(v => {
                let index = array.findIndex((e: any) => e[props.bingValue] == v)
                if (index <= -1) {
                  if (props.bingValueFindType == 'array') {
                    ids.push(v)
                  } else {
                    doQueryDetails(v)
                  }
                }else{
                  recordList.push(array[index])
                }
              })
              //TODO 初始化暴露选中数组对象 当前暴露方法都只支持初始化下拉菜单存在时的数据 待升级doQueryDetails中暴露
              if(props.onChangeRecord){
                props.onChangeRecord(recordList)
              }
              if (props.bingValueFindType == 'array') {
                doQueryDetails(ids)
              }
            } else {
              // 初始化暴露选中对象优化
              let record = array.find((e: any) => e[props.bingValue] == props.value)
              if (record) {
                if(props.onChangeRecord){
                  props.onChangeRecord(record)
                }
              } else {
                doQueryDetails(props.value)
              }
            }
          }
          setPropsOptions()
        })
      }

    }, { immediate: true })

    watch(() => props.options, (val) => {
      if (val && !props.findUrl) {
        options.value = val
        initOptionsList.value = JSON.parse(JSON.stringify(val))
      }
    }, { immediate: true })

    /** 处理禁用选项 */
    watch(()=>props.disabledKeys,(val)=>{
      options.value.map(v=>{
        if(val.includes((v.value) as any)){
          v.disabled = true
        }else{
          v.disabled = false
        }
      })
    },{immediate:true,deep:true})

    // 渲染下拉菜单组件
    const renderOptions = (options) => {
      // 个性化渲染多个label的options
      /*  注： select组件会默认把SelectOption 下的span标签组件作为选中时和占位符中显示的组件，
      只需要把不需要展示的标题组件名称换成其他的即可不在选中时显示，反之需要写样式，但是写样式
      父级写了子组件的class名不理解为什么子组件不生效，但是写标签选择器却可以生效？？？ 个人方法
      使用一个生僻的h5标签比如：aside  然后在父组件的样式中直接写这个标签选择器的样式即可生效也不
      容易影响自带的组件 */
      return () => [
        ...options.map(item => {
          return h(SelectOption,
            { value: item.value, class: less['multipleLabel-select-item-option-content'] },
            {
              default: () => {
                return [
                  h('span', {
                    title: item.label,
                    style: {
                      overflow: 'hidden',
                      whiteSpace: 'nowrap',
                      textOverflow: 'ellipsis'
                    }
                  }, item.label),
                  h('div', {
                    title: item.multipleLabel,
                    style: {
                      overflow: 'hidden',
                      whiteSpace: 'nowrap',
                      textOverflow: 'ellipsis'
                    }
                  }, item.multipleLabel)
                ]
              }
            })
        })
      ]
    }
    return () => {
      const _props: any = {
        ...props,
        options: !props.multipleLabel ? options.value : undefined, //如果存在多标题模式则不传递该属性即 undefined
        filterOption: !props.showSearch,
      }

      
      const on = {
        onChange: handleChange,
        onPopupScroll: handlePopupScroll,
        onSearch: props.showSearch ? handleSearch : undefined,
        onSelect: handleSelect,
      }
      // 用于自定义渲染options数据
      const _options = options.value || []
      return (
        h(Select, 
          {
          class: less.select,
          ..._props,
          ...on,
        },
        !props.multipleLabel ? { ...useSlots() } : renderOptions(_options)) //如果存在多标题模式则使用renderOptions渲染options
      )
    }
  },
})

export default ZSelect