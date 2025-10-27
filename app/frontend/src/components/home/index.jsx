import './home.css'
import references from "../../ref.json"
import { Button } from '@mui/material'
import { Link } from 'react-router-dom'


const  References = () => {
  return (
    <div className='box' style={{ marginTop: 'auto', marginLeft: 'auto', marginRight: 'auto' }}>
        <h2>References</h2>
        <ol>
        {references.map((ref) => {
          const authors = ref.author.join(", ");
          const title = ref.title;
          const journalInfo = ref.journal
            ? `${ref.journal}${ref.volume ? `, ${ref.volume}` : ""}${ref.pages ? `, ${ref.pages}` : ""}`
            : "";
          const year = ref.year ? `(${ref.year})` : "";
          const doiLink = ref.url || (ref.doi ? `https://doi.org/${ref.doi}` : null);

          return (
              <li key={ref.id}>
              {authors}. <strong>{title}</strong>. {journalInfo} {year}{" "}
              {doiLink && (
                  <a href={doiLink} target="_blank" rel="noopener noreferrer">
                  [link]
                  </a>
              )}
              </li>
          );
        })}
        </ol>
    </div>
  );
}

const Home = () => {
    return (
        <div className='home' style={{ display: 'flex', flexDirection: 'column', minHeight: '90vh', padding: '1em', marginLeft: '10%', marginRight: '10%' }}>
          <div className="content" style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-around' }}> 
            <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-around', alignItems: 'center' }}>
              <div className="box" style={{ height: '200px', width: '200px', backgroundColor: 'rgba(0, 0, 0, 0.8)', paddingLeft: '10%' }}>
                <h3 style={{ textAlign: 'center', fontSize: '30px' }}>DATABASES</h3>
                <ul style={{ listStyleType: 'none', padding: 0, textAlign: 'center',}}>
                  <li>
                    <a href="https://www.cosmos.esa.int/web/gaia/data-release-3" target="_blank" rel="noopener noreferrer">Gaia</a>
                  </li>
                  <li>
                    <a href="https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=STELLARHOSTS" target="_blank" rel="noopener noreferrer">NASA Exoplanet Archive</a>
                  </li>
                </ul>
              </div>
              <Link to="/predict">
                  <Button 
                    variant="contained" 
                    sx={{ 
                      backgroundColor: '#CE8236', 
                      '&:hover': { backgroundColor: '#B56B2C' }, 
                      marginTop: '1rem' 
                    }}
                  >
                    Try Predicting
                  </Button>
                </Link>

            </div>
              
                <div className='box' id='intro-box'>
              <h2 style={{ marginBottom: '2rem', textAlign: 'center', fontSize: '30px'}}>Introduction to Data Science mini-project</h2>
              <p style={{ marginBottom: '2rem', textAlign: 'center'}}>
                  This is a group project made on the <a href="https://studies.helsinki.fi/courses/course-unit/otm-f1abc596-92c2-43ec-b42e-dc8114b5247d" target="_blank">Introduction to Data Science</a> course
                  by the University of Helsinki.
              </p>
              <div className='content'>
                  Rocky planets similar to our Earth, are key candidates in the search for extraterrestrial life because of their ability to support conditions necessary for life as we know it -- liquid
                  water, a stable atmosphere and a diverse chemical composition. Whether these planets form, become habitable, and when they do, remain habitable for long enough for life to emerge 
                  and evolve depends on the mass of the host star, which is associated with characteristics such as the intensity of ionizing radiation, known to be very damaging to most lifeforms
                  familiar to us, as well as the star's lifetime, which sets natural boundaries for the existence of potential life within its system. Accurately estimating the masses of a large 
                  number of stars is therefore of great importance in efficiently directing our search for life among the stars.
              </div>
            </div></div>
              
            <References style={{ padding: '0.5em 1em' }}/>
        </div>
    )
}

export default Home