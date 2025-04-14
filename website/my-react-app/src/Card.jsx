import profilePic from './assets/red.jpg';

export default function Card() {
    return(
        <div className='card'>
            <img className='card-image' src={profilePic} alt="profile picture"></img>
            <h2 className='card-title'>Red</h2>
            <p className='card-text'>Red is the main protagonist of Pokémon Red
                and Blue, the first two games in the Nintendo's
                Pokémon franchise, as well as the Pokémon Green and Yellow sequels.</p>
        </div>
    );
}
