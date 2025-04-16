export default function List() {
    // object
    const pokemons = [
        {id: 1, name: 'bulbasaur', type: 'grass'},
        {id: 2, name: 'charmander', type: 'fire'},
        {id: 3, name: 'squirtle', type: 'water'},
        {id: 4, name: 'pikachu', type: 'electric'},
    ];

    // sort
    pokemons.sort((a, b) => a.name.localeCompare(b.name));

   // const listItem = pokemons.map((poke) => <li>{poke}</li>);
    const listItem = pokemons.map((poke) => <li key={poke.id}>
                                               <b>{poke.name}: {poke.type}</b></li>)

    return <ol>{listItem}</ol>;
}
