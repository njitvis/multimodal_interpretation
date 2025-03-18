/* eslint-disable @typescript-eslint/no-unused-vars */
'use client';

import * as d3 from 'd3';
import React, { useEffect, useRef, useState } from 'react';

const HorizontalBar = ({ d }: HorizontalBarProps) => {
	const svgRef = useRef(null);
	const [data, setData] = useState(d);

	useEffect(() => {
		if (data.length > 0) {
			const margin = { top: 50, right: 0, bottom: 0, left: 10 };
			// const margin = { top: 50, right: 100, bottom: 50, left: 100 };
			const parent = svgRef.current.parentNode;
			const width = parent.clientWidth - margin.left - margin.right;
			const height = parent.clientHeight - margin.top - margin.bottom;

			const svg = d3
				.select(svgRef.current)
				.append("svg")
				.attr("width", width + margin.left + margin.right)
				.attr("height", height + margin.top + margin.bottom)
				.append("g")
				.attr("transform", `translate(${margin.left},${margin.top})`);

			const rows = data.map((d) => d.category);
			const cols = data.map((d) => d.value);

			const x = d3.scaleLinear()
				.domain([0, 5])
				.range([0, width]);

			svg.append("g")
				.attr("transform", `translate(0, 0)`)
				.call(d3.axisTop(x).ticks(6).tickFormat(d3.format("d")))
				.selectAll("text")
				.attr("transform", "translate(0, 0)")
				.style("text-anchor", "end");

			svg
				.append("text")
				.attr("class", "x-axis-title")
				.attr(
					"transform",
					`translate(${width / 2}, -${margin.top / 2})`
				)
				.attr("text-anchor", "middle")
				.text("Interpretability")
				.style("font-size", "14px")
				.style("font-weight", "bold");

			const y = d3.scaleBand()
				.range([0, height])
				.domain(rows)
				.padding(.1);

			svg.append("g")
				.call(d3.axisLeft(y))

			svg.append("g")
				.selectAll()
				.data(data)
				.join("rect")
				.attr("x", x(0))
				.attr("y", (d) => y(d.category))
				.attr("width", (d) => x(d.value))
				.attr("height", y.bandwidth())
				.attr("fill", "#69b3a2")
		}

		return () => {
			d3.select(svgRef.current).selectAll("*").remove();
		};
	}, [data]);

	useEffect(() => {
		setData(d);
	}, [d]);


	return (
		<svg ref={svgRef} style={{ width: "100%", height: "100%" }} />
	);
};

interface HorizontalBarProps {
	d: unknown;
};

export default HorizontalBar;