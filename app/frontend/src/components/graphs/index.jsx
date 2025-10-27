import { useState } from "react" 
import Box from '@mui/material/Box'
import Stepper from '@mui/material/Stepper'
import Step from '@mui/material/Step'
import StepButton from '@mui/material/StepButton'
import Button from '@mui/material/Button'

const graphPageStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '4em',
    backgroundColor: "rgba(0, 0, 0, 0.8)"
}

const graphs_description = [
    {
        title: "Gaia and NEA Stellar Properties Comparison",
        description: "Before joining the datasets, we first examined how the stars' properties differed, in order to decide which source to primarily use for each property. The histograms help to see differences in coverage and concentration of the data.",
        src: ["/compare_before_join.html"]
    },
    {
        title: "Outliers in Stellar Properties",
        description: (
            <>
                Another set of graphs that turned out to be useful in improving the datasets were <a href="https://github.com/ala-zukowska/stellar-mass-prediction/tree/main/modeling/eda/output/outliers">outlier graphs</a>. This particular graph was generated before the final data cleaning and showcases a significant outlier in stelar mass. After further investigation, we found that <a href="https://simbad.u-strasbg.fr/simbad/sim-id?Ident=2MASS+J04372171%2B2651014">this star</a> was misclassified and actually falls outside of the main sequence, which is focus of our model.
            </>
        ),
        src: ["/outliers_M.html"]
    },
    {
        title: "Spectral Types in the Dataset",
        description: (
            <>
                One of the first data analyses we did was looking at <a href="https://github.com/ala-zukowska/stellar-mass-prediction/tree/main/modeling/eda/output/single_distributions">single variables distributions:</a> luministy, mass, metallicity, radius, temperature and spectral types of stars. This graph visualizes how many stars fall into each spectral type, which helps in understanding data sample composition.
            </>
        ),
        src: ["/categorical_spectype.html"]
    },
    {
        title: "Pairwise Relationships Analysis",
        description: "After exploring individual variables, we moved on to examine how they relate to each other. These pairwise plots visualize correlations between key stellar properties, with regression lines highlighting overall trends. This step helped us better understand how different stellar features interact and which relationships are strongest within the dataset.",
        src: ["/pairwise.html"]
    },
    {
        title: "Collinearity Check",
        description: "To ensure that the linear regression model would not be affected by highly correlated inputs, we performed a collinearity analysis. The heatmap shows the correlation coefficients between variables, helping us identify which features carry overlapping information (in orange - strong positive correlation). This guided the selection of independent variables for our model.",
        src: ["/collinearity.html"]
    },
    {
        title: "3D View of Stellar Properties",
        description: "Building on the pairwise relationships, we extended the analysis into 3D to see how several stellar properties interact simultaneously.\nThe first plot (Effective Temperature vs. Luminosity vs. Mass) was chosen to illustrate the structure of the main sequence, as these parameters are strongly connected through stellar evolution, and show a clear linear trend across different spectral types.\nThe second plot (Luminosity vs. Metallicity vs. Mass) highlights how stars of different spectral types separate into distinct bands, and corresponds directly to the variables used in our predictive model, where luminosity and metallicity serve as inputs for estimating stellar mass.",
        src: ["/3d_scatter_plot_1.html", "/3d_scatter_plot_2.html"]
    },
]


const GraphVisualisation = ({title, description, srcs = [], height = 600}) => {
    return (
        <div>
            <h2 style={{ marginBottom: '1rem' }}>{title}</h2>
            <p style={{ marginBottom: '2rem' }}>{description}</p>
            {srcs.map((src, index) => (
                <iframe
                    key={index}
                    src={src}
                    width="100%"
                    height={height}
                    title={title}
                    style={{ border: 'none', scrollbarWidth: 'none' }}
                />

            ))}
            
        </div>
    )
}

const Graphs = () => {
  const [activeStep, setActiveStep] = useState(0);
  const totalSteps = graphs_description.length;

  const handleNext = () => {
    setActiveStep((prev) => Math.min(prev + 1, totalSteps - 1));
  };

  const handleBack = () => {
    setActiveStep((prev) => Math.max(prev - 1, 0));
  };

  const handleStep = (step) => () => {
    setActiveStep(step);
  };

  const currentGraph = graphs_description[activeStep];

  return (
    <div style={{ width: '80%', margin: '0 auto' }}>
        <div style={graphPageStyle}>
            <p style={{ marginBottom: '2rem', marginTop: '3rem' }}>
                This page contains interactive graphs visualizing our stellar data, allowing you to explore relationships and patterns between different star properties. The graphs shown here were selected from those we produced during data exploration; for the full collection, visit our  <a href="https://github.com/ala-zukowska/stellar-mass-prediction/tree/main/modeling/eda/output">GitHub repository</a>.
            </p>
        </div>
        <Box sx={{ width: '100%', color: 'white', marginBottom: '3rem' }}>
        <Stepper nonLinear activeStep={activeStep} alternativeLabel >
            {graphs_description.map((_, index) => (
            <Step 
                key={index}
                sx={{
                    '& .MuiStepLabel-root .Mui-completed': {
                        color: '#A1420C', // circle color (COMPLETED)
                    },
                    '& .MuiStepLabel-label.Mui-completed.MuiStepLabel-alternativeLabel':
                        {
                        color: '#A1420C', // Just text label (COMPLETED)
                        },
                    '& .MuiStepLabel-root .Mui-active': {
                        color: '#CE8236', // circle color (ACTIVE)
                    },
                    '& .MuiStepLabel-label.Mui-active.MuiStepLabel-alternativeLabel':
                        {
                        color: '#CE8236', // Just text label (ACTIVE)
                        },
                    '& .MuiStepLabel-root .Mui-active .MuiStepIcon-text': {
                        fill: '#DDD', // circle's number (ACTIVE)
                    },
                    }}
            >
                <StepButton color="inherit" onClick={handleStep(index)} />
            </Step>
            ))}
        </Stepper>

        <Box sx={{ display: 'flex', justifyContent: 'space-around', mt: 2 }}>
            <Button
            color="inherit"
            disabled={activeStep === 0}
            onClick={handleBack}
            >
            Back
            </Button>
            <Button
            color="inherit"
            disabled={activeStep === totalSteps - 1}
            onClick={handleNext}
            >
            Next
            </Button>
        </Box>

        <div style={graphPageStyle}>
            <GraphVisualisation
            title={currentGraph.title}
            description={currentGraph.description}
            srcs={currentGraph.src}
            />
        </div>
        </Box>
    </div>
  );
}

export default Graphs