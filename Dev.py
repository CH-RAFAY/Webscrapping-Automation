import pandas as pd
import random
import json
import webbrowser
import os

# Data generation code
def generate_hotel_data(num_hotels=50):
    hotel_names = [f"Hotel {chr(65 + i) if i < 26 else chr(65 + (i//26 - 1)) + chr(65 + (i%26))}" for i in range(num_hotels)]
    data = {
        'Name': hotel_names,
        'Location': ['New York'] * num_hotels,
        'Rating': [round(random.uniform(3.0, 5.0), 1) for _ in range(num_hotels)],
        'Price': [random.randint(100, 500) for _ in range(num_hotels)],
        'Link': [f"https://example.com/hotel_{i}" for i in range(num_hotels)]
    }
    return pd.DataFrame(data)

# Generate data
df = generate_hotel_data(50)
df.to_csv('hotels.csv', index=False)
hotels_json = df.to_dict('records')
hotels_json_str = json.dumps(hotels_json)

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Interactive Hotel Knowledge Graph</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
    <style>
        body {
            margin: 0;
            overflow: hidden;
            background-color: #f8fafc;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        }
        #container {
            width: 100vw;
            height: 100vh;
            overflow: auto;
        }
        #graph {
            width: 300%;
            height: 300%;
            min-width: 3000px;
            min-height: 3000px;
            background-color: #ffffff;
            background-image: radial-gradient(#f1f5f9 1px, transparent 1px);
            background-size: 30px 30px;
        }
        .tooltip {
            position: fixed;
            padding: 12px 16px;
            background-color: rgba(255, 255, 255, 0.98);
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            pointer-events: none;
            font-size: 14px;
            max-width: 300px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            z-index: 1000;
            transition: all 0.2s ease;
            opacity: 0;
        }
        .node {
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .link {
            transition: all 0.2s ease;
        }
        .node-label {
            font-weight: 800;
            pointer-events: none;
            text-shadow: 0px 1px 2px rgba(255,255,255,0.9);
        }
        .controls {
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 1000;
            background: rgba(255, 255, 255, 0.98);
            padding: 12px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            backdrop-filter: blur(8px);
        }
        button {
            margin: 0 4px;
            padding: 8px 16px;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            background: white;
            cursor: pointer;
            font-weight: 600;
            font-size: 14px;
            color: #1e293b;
            transition: all 0.2s ease;
        }
        button:hover {
            background: #f8fafc;
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
    </style>
</head>
<body>
    <div class="controls">
        <button onclick="zoomIn()">Zoom In</button>
        <button onclick="zoomOut()">Zoom Out</button>
        <button onclick="resetZoom()">Reset</button>
    </div>
    <div id="container">
        <div id="graph"></div>
    </div>
    <div class="tooltip"></div>
    <script>
        const hotels = HOTELS_DATA_PLACEHOLDER;  // Will be replaced with actual data
        const nodes = [];
        const links = [];
        const tooltip = d3.select(".tooltip");

        // Find price range for scaling
        const prices = hotels.map(h => h.Price);
        const minPrice = Math.min(...prices);
        const maxPrice = Math.max(...prices);

        // Create color scale for price-based edges
        const priceColorScale = d3.scaleLinear()
            .domain([minPrice, maxPrice])
            .range(["#e5e7eb", "#4b5563"]);  // Light grey to dark grey

        // Root node
        nodes.push({
            id: "New York",
            label: "NY",
            type: "location",
            full: "New York City",
            radius: 45
        });

        // Create nodes and links
        hotels.forEach((hotel, idx) => {
            nodes.push({
                id: hotel.Name,
                label: `H${idx + 1}`,
                type: "hotel",
                full: `${hotel.Name}\\nPrice: $${hotel.Price}\\nRating: ${hotel.Rating}★`,
                radius: 30,
                price: hotel.Price
            });

            // Price-based colored edge from location to hotel
            links.push({
                source: "New York",
                target: hotel.Name,
                color: priceColorScale(hotel.Price),
                isMainEdge: true,
                width: 2.5
            });

            const attributes = [
                { key: 'price', label: 'P', value: `$${hotel.Price}`, color: 'rgba(220, 38, 127, 0.95)' },
                { key: 'rating', label: 'R', value: `${hotel.Rating}★`, color: 'rgba(34, 139, 34, 0.95)' },
                { key: 'link', label: 'L', value: hotel.Link, color: 'rgba(106, 90, 205, 0.95)' }
            ];

            attributes.forEach(attr => {
                const nodeId = `${hotel.Name}_${attr.key}`;
                nodes.push({
                    id: nodeId,
                    label: attr.label,
                    type: "attribute",
                    attrType: attr.key,
                    full: `${attr.value}`,
                    radius: 22
                });

                links.push({
                    source: hotel.Name,
                    target: nodeId,
                    color: attr.color,
                    isChildEdge: true,
                    width: 3.5  // Increased width for child edges
                });
            });
        });

        const container = document.getElementById('container');
        const width = Math.max(container.clientWidth * 3, 3000);
        const height = Math.max(container.clientHeight * 3, 3000);
        
        const svg = d3.select("#graph")
            .append("svg")
            .attr("width", width)
            .attr("height", height);

        const simulation = d3.forceSimulation(nodes)
            .force("charge", d3.forceManyBody().strength(-4500))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("link", d3.forceLink(links).id(d => d.id).distance(280))
            .force("collide", d3.forceCollide().radius(d => d.radius * 6));

        const link = svg.append("g")
            .selectAll("line")
            .data(links)
            .join("line")
            .attr("class", "link")
            .style("stroke", d => d.color)
            .style("stroke-width", d => `${d.width}px`)
            .style("opacity", 0.8);

        const node = svg.append("g")
            .selectAll("g")
            .data(nodes)
            .join("g")
            .attr("class", "node")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        // Enhanced node styling with bolder appearance
        node.append("circle")
            .attr("r", d => d.radius)
            .style("fill", d => {
                if (d.type === "location") return "#fbbf24";
                if (d.type === "hotel") return "#dbeafe";
                if (d.type === "attribute") {
                    switch(d.attrType) {
                        case 'price': return "#fce7f3";
                        case 'rating': return "#dcfce7";
                        case 'link': return "#ede9fe";
                        default: return "#e0f2fe";
                    }
                }
                return "#e0f2fe";
            })
            .style("stroke", d => {
                if (d.type === "location") return "#b45309";
                if (d.type === "hotel") return "#1d4ed8";
                if (d.type === "attribute") {
                    switch(d.attrType) {
                        case 'price': return "#be185d";
                        case 'rating': return "#15803d";
                        case 'link': return "#5b21b6";
                        default: return "#1e40af";
                    }
                }
                return "#1e40af";
            })
            .style("stroke-width", d => {
                if (d.type === "location") return "5px";
                if (d.type === "hotel") return "4px";
                return "4px";  // Increased border width for all nodes
            })
            .style("filter", "drop-shadow(0px 2px 3px rgba(0,0,0,0.2))");

        node.append("text")
            .attr("class", "node-label")
            .text(d => d.label)
            .attr("text-anchor", "middle")
            .attr("dy", ".35em")
            .style("fill", "#1e293b")
            .style("font-size", d => d.type === "location" ? "18px" : "14px")
            .style("font-weight", "800");

        let currentZoom = 1;
        
        function zoomIn() {
            currentZoom *= 1.2;
            svg.style("transform", `scale(${currentZoom})`);
        }
        
        function zoomOut() {
            currentZoom /= 1.2;
            svg.style("transform", `scale(${currentZoom})`);
        }
        
        function resetZoom() {
            currentZoom = 1;
            svg.style("transform", "scale(1)");
        }

        node.on("mouseover", function(event, d) {
            tooltip
                .style("opacity", 1)
                .html(d.full.replace(/\\n/g, '<br/>'))
                .style("left", (event.pageX + 15) + "px")
                .style("top", (event.pageY - 15) + "px");
            
            const connectedNodes = new Set();
            links.forEach(link => {
                if (link.source.id === d.id) connectedNodes.add(link.target.id);
                if (link.target.id === d.id) connectedNodes.add(link.source.id);
            });
            
            node.selectAll("circle")
                .style("opacity", n => connectedNodes.has(n.id) || n.id === d.id ? 1 : 0.2)
                .style("transform", n => connectedNodes.has(n.id) || n.id === d.id ? "scale(1.1)" : "scale(1)")
                .style("stroke-width", n => {
                    if (connectedNodes.has(n.id) || n.id === d.id) {
                        return n.type === "location" ? "6px" : "5px";
                    }
                    return n.type === "location" ? "5px" : "4px";
                });
            
            link.style("opacity", l => 
                l.source.id === d.id || l.target.id === d.id ? 1 : 0.1)
                .style("stroke-width", l => {
                    if (l.source.id === d.id || l.target.id === d.id) {
                        return l.isChildEdge ? "4.5px" : "3.5px";
                    }
                    return l.isChildEdge ? "3.5px" : "2.5px";
                });
        })
        .on("mouseout", function() {
            tooltip.style("opacity", 0);
            
            node.selectAll("circle")
                .style("opacity", 1)
                .style("transform", "scale(1)")
                .style("stroke-width", d => {
                    if (d.type === "location") return "5px";
                    if (d.type === "hotel") return "4px";
                    return "4px";
                });
            
            link.style("opacity", 0.8)
                .style("stroke-width", d => d.isChildEdge ? "3.5px" : "2.5px");
        })
        .on("click", function(event, d) {
            alert(`Full Information:\\n${d.full}`);
        });

        simulation.on("tick", () => {
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node
                .attr("transform", d => `translate(${d.x},${d.y})`);
        });

        function dragstarted(event) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            event.subject.fx = event.subject.x;
            event.subject.fy = event.subject.y;
        }

        function dragged(event) {
            event.subject.fx = event.x;
            event.subject.fy = event.y;
        }

        function dragended(event) {
            if (!event.active) simulation.alphaTarget(0);
            event.subject.fx = null;
            event.subject.fy = null;
        }
    </script>
</body>
</html>
"""

# Replace the placeholder with actual data
html_content = html_template.replace('HOTELS_DATA_PLACEHOLDER', hotels_json_str)

# Save and open the file
html_path = 'hotel_graph.html'
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

webbrowser.open('file://' + os.path.realpath(html_path))

print("Generated 'hotels.csv' and 'hotel_graph.html' successfully with enhanced visualization!")


