import pairwiseRegression from '../../assets/pairwise_with_regression.png'
import pairPlot from '../../assets/pairplot.png'
import collinearity from '../../assets/collinearity.png'
import categoricalSpec from '../../assets/categorical_spectype.png'

const Graphs = () => {
    return (
        <div>
            <h1>Plots</h1>
            <div>
                <h2>Spectral types in the dataset</h2>
                <img width={600} height={600} src={categoricalSpec} alt="counts of spectral types" />
            </div>
            <div>
                <h2>Collinearity</h2>
                <img width={600} height={600} src={collinearity} alt="collinearity" />
            </div>
            <div>
                <h2>Pairwise relationships</h2>
                <img width={600} height={600} src={pairwiseRegression} alt="pairwise regression" />
            </div>
            <div>
                <h2>Pairplot</h2>
                <img width={600} height={600} src={pairPlot} alt="pairplot" />
            </div>
        </div>
    )
}

export default Graphs