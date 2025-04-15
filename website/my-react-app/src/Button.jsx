export default function Button() {
    // Inline
    const styles = {
        backgroundColor: 'hsl(4, 88%, 57%)',
        color: 'black',
        padding: '10px 20px',
        borderRadius: '50px',
        border: 'none',
        cursor: 'pointer',
        margin: '10px',
      }
    
    return (
        <button style = {styles}>Click me</button>
    );
}

/*
css
external index.css:
.button {}
<button className='button'>click me</button>

module Button.module.css:
import styles from './Button.module.css';
return <button className={styles.button}>Click me</button>
*/
