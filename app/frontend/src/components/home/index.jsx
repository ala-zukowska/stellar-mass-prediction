import references from "../../ref.json"

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
    justifyContent: 'center',
    fontSize: 24,
    lineHeight: '1.5',
    padding: '1em 6em'
}


const  References = () => {
  return (
    <div>
        <h2>References</h2>
        <ul>
        {references.map((ref) => {
          const authors = ref.author.join(", ");
          const title = ref.title;
          const journalInfo = ref.journal
            ? `${ref.journal}${ref.volume ? `, ${ref.volume}` : ""}${ref.pages ? `, ${ref.pages}` : ""}`
            : "";
          const year = ref.year ? `(${ref.year})` : "";
          const doiLink = ref.url || (ref.doi ? `https://doi.org/${ref.doi}` : null);

          return (
            <p>
                <li key={ref.id}>
                {authors}. <strong>{title}</strong>. {journalInfo} {year}{" "}
                {doiLink && (
                    <a href={doiLink} target="_blank" rel="noopener noreferrer">
                    [link]
                    </a>
                )}
                </li>
            </p>
          );
        })}
        </ul>
    </div>
  );
}

const Home = () => {
    return (
        <div style={homeStyle}>
            <h2>Introduction to Data Science mini-project</h2>
            <p>
                This is a group project made on the <a href="https://studies.helsinki.fi/courses/course-unit/otm-f1abc596-92c2-43ec-b42e-dc8114b5247d" target="_blank">Introduction to Data Science</a> course
                by the University of Helsinki.
            </p>
            <div style={contentStyle}>
                Rocky planets similar to our Earth, are key candidates in the search for extraterrestrial life because of their ability to support conditions necessary for life as we know it -- liquid
                water, a stable atmosphere and a diverse chemical composition. Whether these planets form, become habitable, and when they do, remain habitable for long enough for life to emerge 
                and evolve depends on the mass of the host star, which is associated with characteristics such as the intensity of ionizing radiation, known to be very damaging to most lifeforms
                familiar to us, as well as the star's lifetime, which sets natural boundaries for the existence of potential life within its system. Accurately estimating the masses of a large 
                number of stars is therefore of great importance in efficiently directing our search for life among the stars.
            </div>
            <References style={{ padding: '0.5em 1em' }}/>
        </div>
    )
}

export default Home