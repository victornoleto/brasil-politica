// ECharts with only the modules in use (smaller bundle). Import from here, not from 'echarts'.
import * as echarts from 'echarts/core'
import { BarChart, LineChart, ScatterChart } from 'echarts/charts'
import {
  GraphicComponent, GridComponent, LegendComponent, MarkAreaComponent, MarkLineComponent, TitleComponent, TooltipComponent,
} from 'echarts/components'
import { SVGRenderer } from 'echarts/renderers'
import { LabelLayout } from 'echarts/features'
import { theme } from './colors.js'

echarts.use([
  BarChart, LineChart, ScatterChart, GraphicComponent, GridComponent, LegendComponent, MarkAreaComponent,
  MarkLineComponent, TitleComponent, TooltipComponent, SVGRenderer, LabelLayout,
])

export const FONT = "'IBM Plex Sans', system-ui, sans-serif"

/** Applies the theme font and colors to the chart text and tooltip (ECharts does not inherit from CSS). */
export function withFont(op) {
  const t = theme()
  return {
    ...op,
    textStyle: { fontFamily: FONT, ...op.textStyle },
    ...(op.tooltip && {
      tooltip: {
        backgroundColor: t.surface, borderColor: t.axis,
        ...op.tooltip,
        textStyle: { fontFamily: FONT, color: t.ink, ...op.tooltip.textStyle },
      },
    }),
  }
}

export default echarts
