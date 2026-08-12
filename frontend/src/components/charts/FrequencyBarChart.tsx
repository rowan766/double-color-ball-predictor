import * as echarts from 'echarts';
import { useEffect, useRef } from 'react';
import type { FrequencyItem } from '../../types/analysis';

interface FrequencyBarChartProps {
  data: FrequencyItem[];
  color: string;
}

export function FrequencyBarChart({ data, color }: FrequencyBarChartProps) {
  const ref = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!ref.current) {
      return;
    }
    const chart = echarts.init(ref.current);
    chart.setOption({
      grid: { left: 40, right: 16, top: 16, bottom: 32 },
      xAxis: { type: 'category', data: data.map((item) => item.number.toString().padStart(2, '0')) },
      yAxis: { type: 'value' },
      tooltip: { trigger: 'axis' },
      series: [
        {
          type: 'bar',
          data: data.map((item) => item.count),
          itemStyle: { color },
        },
      ],
    });
    const handleResize = () => chart.resize();
    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
      chart.dispose();
    };
  }, [color, data]);

  return <div className="chart" ref={ref} />;
}
