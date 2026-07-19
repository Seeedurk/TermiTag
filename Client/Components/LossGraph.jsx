import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function LossGraph({data}) {
	return (
		<LineChart width={300} height={200} data={data}>
			<CartesianGrid strokeDasharray="3 3" />
			<XAxis dataKey="step" />
			<YAxis domain={[0, 'dataMax']} />
			<Tooltip />
			<Line 
				type="monotone" 
				dataKey="loss" 
				stroke="#4da6ff" 
				strokeWidth={2} 
				dot={false}
				isAnimationActive={false}
			/>
		</LineChart>
	)
}

export default LossGraph;