

const Def = () => {
    return (
        <div style={{ backgroundColor: 'lightGray', padding: '1em' }}>
            <h1>Definitions</h1>
            <div>
                <h2>Luminosity: </h2>
                Total outgoing power radiated by a star. Usually expressed in solar luminosities (1 L_sun = 3.828 * 10^26 W).
            </div>
            <div>
                <h2>Metallicity (Fe/H): </h2>
                Ratio of atoms of iron to atoms of hydrogen within a star. Expressed on a logarithmic scale. The metallicity of the Sun is approximately
                -4.54, meaning that the ratio of iron to hydrogen is approximately 10^-4.54 in terms of individual atoms. The metallicity of main sequence stars usually falls
                between around -4 to -7, although extremely old stars originating from the early days of the universe can have values far below the lower bound.
            </div>
            <div>
                <h2>Mass:</h2>
                The mass of a star. Expressed in solar masses (1 M_sun = 1.99 * 10^30 kg).
            </div>
            <div>
                <h2>Radius:</h2>
                The radius of a star. Expressed in solar radii (1 R_sun = 6.96 * 10^8 m).
            </div>
            <div>
                <h2>Teff: </h2>
                The estimated surface temperature of a star derived from a black body approximation.
            </div>
            <div>
                <h2>Spectral classsification: </h2>
                Classification of stars based on their surface temperature. The industry standard Harvard classification includes
                the following classes (descending): O, B, A, F, G, K, M.
            </div>
            <div>
                <h2>Main sequence star: </h2>
                A relatively stable star that produces energy through hydrogen fusion. This is the longest lasting phase
                in a stellar life cycle.
            </div>
            <div>
                <h2>Mass-luminosity relation: </h2>
                An empirically established relationship between the mass and luminosity of a main sequence star.
            </div>
        </div>
    )
}

export default Def