import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

const DefinitionCard = ({title, description}) => {
    return (
        <Card sx={{ width: 320, height: 320, backgroundColor: 'rgba(0, 0, 0, 0.8)', m: 2, }}>
            <CardContent>
            <Typography variant="h5" component="div" sx={{ color: '#CE8236', fontFamily: '"Quattrocento Sans", sans-serif', mb: 2, textAlign: 'center' }}>
                {title}
            </Typography>
            <Typography variant="body2" sx={{ color: '#ddd', fontFamily: '"Quattrocento Sans", sans-serif', }}>
                {description}
            </Typography>
            </CardContent>
        </Card>
    )
}

const definitions = [
  {
    title: 'Luminosity',
    description:
      'Total outgoing power radiated by a star. Usually expressed in solar luminosities (1 L_sun = 3.828 × 10^26 W).',
  },
  {
    title: 'Metallicity (Fe/H)',
    description:
      'Ratio of atoms of iron to atoms of hydrogen within a star. Expressed on a logarithmic scale. The metallicity of the Sun is approximately -4.54, meaning that the ratio of iron to hydrogen is approximately 10^-4.54 in terms of individual atoms. The metallicity of main sequence stars usually falls between around -4 to -7, although extremely old stars originating from the early days of the universe can have values far below the lower bound.',
  },
  {
    title: 'Mass',
    description:
      'The mass of a star. Expressed in solar masses (1 M_sun = 1.99 × 10^30 kg).',
  },
  {
    title: 'Radius',
    description:
      'The radius of a star. Expressed in solar radii (1 R_sun = 6.96 × 10^8 m).',
  },
  {
    title: 'Teff',
    description:
      'The estimated surface temperature of a star derived from a black body approximation.',
  },
  {
    title: 'Spectral classification',
    description:
      'Classification of stars based on their surface temperature. The industry standard Harvard classification includes the following classes (descending): O, B, A, F, G, K, M.',
  },
  {
    title: 'Main sequence star',
    description:
      'A relatively stable star that produces energy through hydrogen fusion. This is the longest lasting phase in a stellar life cycle.',
  },
  {
    title: 'Mass-luminosity relation',
    description:
      'An empirically established relationship between the mass and luminosity of a main sequence star.',
  },
];

const Def = () => {
    return (
    <div style={{ padding: '1em' }}>
      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
        }}
      >
        {definitions.map((def, index) => (
          <DefinitionCard key={index} title={def.title} description={def.description} />
        ))}
      </div>
    </div>
  )
}

export default Def