const graphPageStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '4em',
    border: 'solid gray',
    backgroundColor: 'lightgray'
}

const graphs_description = [
    {
        title: "Gaia and NEA Stellar Properties Comparison",
        description: "Before joining the datasets, we first examined how the stars' properties differed to decide which source to primarily use for each property. The histograms help to see differences in coverage and concentration of the data.",
        src: ["/compare_before_join.html"]
    },
    {
        title: "Outliers in Stellar Properties",
        description: (
            <>
                Another set of graphs that proved useful in refining the datasets were <a href="https://github.com/ala-zukowska/stellar-mass-prediction/tree/main/modeling/eda/output/outliers">outlier graphs</a>. This particular graph was generated before the final data cleaning and showcases a significant outlier in stelar mass. After further investigation, we found that <a href="https://simbad.u-strasbg.fr/simbad/sim-id?Ident=2MASS+J04372171%2B2651014">this star</a> was misclassified and actually falls outside of the main sequence, which is focus of our model.
            </>
        ),
        src: ["/outliers_M.html"]
    },
    {
        title: "Spectral Types in the Dataset",
        description: (
            <>
                One of the first data analyses we did was looking at <a href="https://github.com/ala-zukowska/stellar-mass-prediction/tree/main/modeling/eda/output/single_distributions">single variables distributions:</a> luministy, mass, metallicity, radius, temperature and spectral types of stars, all of which roughly follow the normal distribution. This graph visualizes how many stars fall into each spectral type, which helps in understanding data sample composition.
            </>
        ),
        src: ["/categorical_spectype.html"]
    },
    {
        title: "Pairwise Relationships Analysis",
        description: "After exploring individual variables, we moved on to examine how they relate to each another. These pairwise plots visualize correlations between key stellar properties, with regression lines highlighting overall trends. This step helped us better understand how different stellar features interact and which relationships are strongest within the dataset.",
        src: ["/pairwise.html"]
    },
    {
        title: "Collinearity Check",
        description: "To ensure that the linear regression model would not be affected by highly correlated inputs, we performed a collinearity analysis. This heatmap shows the correlation coefficients between variables, helping us identify which features carry overlapping information (in orange - strong positive correlation). This guided the selection of independent variables for our model.",
        src: ["/collinearity.html"]
    },
    {
        title: "3D View of Stellar Properties",
        description: "Building on the pairwise relationships, we extended the analysis into 3D to see how several stellar properties interact simultaneously. The first plot (Effective Temperature – Luminosity – Mass) was chosen to illustrate the structure of the main sequence, as these parameters are strongly connected through stellar evolution and reveal a clear linear trend across different spectral types. The second plot (Luminosity – Metallicity – Mass) highlights how stars of different spectral types separate in this feature space and corresponds directly to the variables used in our predictive model, where luminosity and metallicity serve as inputs for estimating stellar mass.",
        src: ["/3d_scatter_plot_1.html", "/3d_scatter_plot_2.html"]
    },
]


const GraphVisualisation = ({title, description, srcs = [], height = 700}) => {
    return (
        <div style={{ marginBottom: '2rem' }}>
            <h2>{title}</h2>
            <p>{description}</p>
            {srcs.map((src, index) => (
                <iframe
                    key={index}
                    src={src}
                    width="100%"
                    height={height}
                    title={title}
                    style={{ border: 'none' }}
                />

            ))}
            
        </div>
    )
}

const Graphs = () => {
    return (
        <div style={graphPageStyle}>
            <h1>Plots</h1>
            <p>
                This page contains interactive graphs visualizing our stellar data, allowing you to explore 
                relationships and patterns between different star properties. The graphs shown here were selected 
                from those we produced during data exploration; for the full collection, visit our <a href="https://github.com/ala-zukowska/stellar-mass-prediction/tree/main/modeling/eda/output">GitHub repository</a>.
            </p>
            {graphs_description.map((graph,index)=>(
                <GraphVisualisation key={index} title={graph.title} description={graph.description} srcs={graph.src}/>
            ))} 
        </div>
    )
}

export default Graphs