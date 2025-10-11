
const homeStyle = {
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: 'lightgray',
    justifyContent: 'center',
    alignItems: 'center',
    color: 'black',
    padding: '1em',
}

const contentStyle = {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'left',
    gap: '10em'
}

const columnStyle = {
    padding: '2em'
}

const Home = () => {
    return (
        <div style={homeStyle}>
            <h2>Introduction to Data Science mini-project</h2>
            <p>
                This is a group project made on the <a href="https://studies.helsinki.fi/courses/course-unit/otm-f1abc596-92c2-43ec-b42e-dc8114b5247d" target="_blank">Introduction to Data Science</a> course
                by the University of Helsinki.
            </p>
            <p style={{ fontSize: 18 }}>
                This website provides a user-interface to our linear regression model that predicts the stellar mass of a star. The input variables of the model are 
                the metallicity and luminosity of the star.
            </p>
            <div style={contentStyle}>
                <div style={columnStyle}>
                    <h3>Dataset: </h3>
                    This is where the dataset is introduced.
                </div>
                <div style={columnStyle}>
                    <h3>Results:</h3>
                    Some discussion of the results
                </div>
            </div>
        </div>
    )
}

export default Home