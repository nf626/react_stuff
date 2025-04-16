import profilePic2 from './assets/blue.jpg'

export default function Card2() {
    return(
        <div className='card2'>
            <img className='card-image2' src={profilePic2} alt='profile picture 2'></img>
            <h2 className='card-title2'>Blue</h2>
            <p className='card-text2'>
            Blue Oak is the rival of the player in the Generation I games,
            as well as in Pokémon FireRed and LeafGreen,
            their Generation III remakes.
            By the end of the main game in these games,
            he also becomes the Pokémon Champion of the Indigo Plateau.
            </p>
        </div>
    );
}
