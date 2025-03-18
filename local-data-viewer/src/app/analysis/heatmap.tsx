/* eslint-disable @typescript-eslint/no-explicit-any */

'use client';

import * as d3 from 'd3';
import React, { useEffect, useState, useRef } from 'react';

const Heatmap = ({ data, x_cat }: HeatmapProps) => {
	const svgRef = useRef(null);
	const [formattedData, setFormattedData] = useState<[]>([]);
	const [hoveredRow, setHoveredRow] = useState<string | null>(null);

	useEffect(() => {
		setFormattedData(
			data.map(d => {
				const vectors = d["vectors"].reduce((acc: number[], item: number, index: number) => {
					acc[index + 1] = item / d["vectors"].reduce((accumulator, current) => accumulator + current, 0);
					return acc;
				}, {} as { [key: number]: number });

				return {
					id: d.id,
					...vectors
				}
			})
		);
	}, [data]);

	useEffect(() => {
		if (formattedData.length > 0) {
			const margin = { top: 50, right: 0, bottom: 0, left: 0 };
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

			const rows = formattedData.map((d) => d.id);
			const cols = Object.keys(formattedData[0]).filter(key => key !== "id");

			const x = d3.scaleBand().domain(cols).range([0, width]).padding(0);
			const y = d3.scaleBand().domain(rows).range([0, height]).padding(0);

			svg.append("g")
				.call(d3.axisTop(x).tickFormat((d, i) => x_cat? x_cat[i] || d : d))
				.attr("class", "x-axis")
				.selectAll("text")
				.style("text-anchor", "middle")
				.style("font-size", "12px");


			svg
				.append("text")
				.attr("class", "x-axis-title")
				.attr(
					"transform",
					`translate(${width / 2}, -${margin.top / 2})`
				)
				.attr("text-anchor", "middle")
				.text("Vectors")
				.style("font-size", "14px")
				.style("font-weight", "bold");

			svg
				.append("text")
				.call(d3.axisLeft(y).ticks(0))
				.attr("class", "y-axis-title")
				.attr(
					"transform",
					`translate(-${margin.left / 2}, ${height / 2}) rotate(-90)`
				)
				.attr("text-anchor", "middle")
				.text("Captions")
				.style("font-size", "14px")
				.style("font-weight", "bold");

			const colorScale = d3
				.scaleLinear()
				.domain([0, 1])
				.range(["#d6e0ff", "blue"]);

			// Create a group for the heatmap cells
			const cells = svg
				.selectAll()
				.data(formattedData.flatMap((row) =>
					cols.map((col) => ({ x: col, y: row.id, value: row[col] }))
				))
				.enter()
				.append("rect")
				.attr("x", (d) => x(d.x))
				.attr("y", (d) => y(d.y))
				.attr("width", x.bandwidth())
				.attr("height", y.bandwidth())
				.style("fill", (d) => colorScale(d.value));

			// Hover functionality for highlighting rows
			cells
				.on("mouseenter", (event, d) => {
					// Highlight the row
					d3.selectAll(`rect`)
						.filter((cell) => cell.y === d.y)
						.style("stroke", "black")
						.style("stroke-width", 2);

					// Set the hovered row id to display row details
					setHoveredRow(d.y);
				})
				.on("mouseleave", () => {
					// Remove the highlight
					d3.selectAll(`rect`)
						.style("stroke", null)
						.style("stroke-width", null);

					// Clear the hovered row details
					setHoveredRow(null);
				});

			// Show details of the hovered row
			if (hoveredRow) {
				const rowData = data.find(row => row.id === hoveredRow);
				if (rowData) {
					// Create or update the tooltip
					svg
						.selectAll(".tooltip")
						.data([hoveredRow])
						.join("text")
						.attr("class", "tooltip")
						.attr("x", width - 150)
						.attr("y", -30)
						.text(`Vector: ${rowData["vectors"]}`)
						.style("font-size", "12px");
				}
			} else {
				// Remove tooltip when no row is hovered
				svg.selectAll(".tooltip").remove();
			}
		}

		return () => {
			d3.select(svgRef.current).selectAll("*").remove();
		};
	}, [formattedData, hoveredRow]);

	return <svg ref={svgRef} style={{ width: "100%", height: "100%" }} />;
};

interface HeatmapProps {
	data: any;
	proportion?: boolean;
	x_cat: string[];
};

export default Heatmap;
