import { ColumnType, CompareFn, SortOrder } from "ant-design-vue/lib/table/interface"
import { TooltipProps } from "ant-design-vue/lib/tooltip/Tooltip"
import { Breakpoint } from "ant-design-vue/lib/_util/responsiveObserve"
import { VueNode } from "ant-design-vue/lib/_util/type"
export interface Column<T = any> {
  /** 设置列的对齐方式 */
  align?: 'left' | 'right' | 'center'
  /** 表头列合并 设置为 0 时，不渲染 */
  colSpan?: number
  /** 设置单元格属性 */
  customCell?: (record: T, rowIndex: number, column: Column) => void
  /** 启用 v - slot: customFilterDropdown，优先级低于 filterDropdown */
  customFilterDropdown?: boolean
  /** 设置头部单元格属性 */
  customHeaderCell?: (column: Column) => void
  /** 生成复杂数据的渲染函数，参数分别为当前行的值，当前行数据，行索引 */
  customRender?: ({ text, record, index, column }: { text: any, record: T, index: number, column: Column }) => any
  /**	列数据在数据项中对应的路径，支持通过数组查询嵌套路径 */
  dataIndex: string | string[]
  /** 默认筛选值 */
  defaultFilteredValue?: string[]
  /** 默认排序顺序 */
  defaultSortOrder?: SortOrder
  /** 
   * 超过宽度将自动省略，暂不支持和排序筛选一起使用 
   * 设置为 true 或 { showTitle ?: boolean } 时，表格布局将变成 tableLayout = "fixed"。
   */
  ellipsis?: boolean | { showTitle?: boolean }
  /** 可以自定义筛选菜单，此函数只负责渲染图层，需要自行编写各种交互 */
  filterDropdown?: VueNode
  /** 用于控制自定义筛选菜单是否可见 */
  filterDropdownVisible?: boolean
  /** 标识数据是否经过过滤，筛选图标会高亮 */
  filtered?: boolean
  /** 筛选的受控属性，外界可用此控制列的筛选状态，值为已筛选的 value 数组	 */
  filteredValue?: string[]
  /** 自定义 filter 图标。 */
  filterIcon?: VueNode | ((opt: {
    filtered: boolean;
    column: ColumnType;
  }) => VueNode);
  /** 指定筛选菜单的用户界面 */
  filterMode?: 'menu' | 'tree'
  /** 是否多选 */
  filterMultiple?: boolean
  /** 表头的筛选菜单项 */
  filters?: object[]
  /** 筛选菜单项是否可搜索 */
  filterSearch?: Boolean
  /** 列是否固定，可选 true(等效于 left) 'left' 'right' */
  fixed?: boolean | string
  /** Vue 需要的 key，如果已经设置了唯一的 dataIndex，可以忽略这个属性 */
  key?: string
  /** 拖动列最大宽度，会受到表格自动调整分配宽度影响 */
  maxWidth?: number
  /** 拖动列最小宽度，会受到表格自动调整分配宽度影响 */
  minWidth?: number
  /** 是否可拖动调整宽度，此时 width 必须是 number 类型 */
  resizable?: boolean
  /** 响应式 breakpoint 配置列表。未设置则始终可见。 */
  responsive?: Breakpoint[]
  /** 表头显示下一次排序的 tooltip 提示, 覆盖 table 中 showSorterTooltip */
  showSorterTooltip?: boolean | TooltipProps
  /** 支持的排序方式，取值为 'ascend' 'descend' */
  sortDirections?: Array<SortOrder>
  /** 排序函数，本地排序使用一个函数(参考 Array.sort 的 compareFunction)，需要服务端排序可设为 true */
  sorter?: boolean | CompareFn<T> | {
    compare?: CompareFn<T>;
    /** Config multiple sorter order priority */
    multiple?: number;
  };
  /** 排序的受控属性，外界可用此控制列的排序，可设置为 'ascend' 'descend' false */
  sortOrder?: boolean | string
  /** 列头显示文字 */
  title?: string
  /** 列宽度 */
  width?: string | number
  /** 本地模式下，确定筛选的运行函数, 使用 template 或 jsx 时作为filter事件使用 */
  onFilter?: Function
  /** 自定义筛选菜单可见变化时调用，使用 template 或 jsx 时作为filterDropdownVisibleChange事件使用 */
  onFilterDropdownVisibleChange?: (visible: boolean) => void
  /**  可以内嵌 children，以渲染分组表头。 */
  children?: Array<Column>,
  /** 是否排除筛选 */
  excludes?: boolean,
  /** 字段可见性 */
  visible?: boolean
  [key: string]: any
}
