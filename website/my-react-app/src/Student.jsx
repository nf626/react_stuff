import PropTypes from 'prop-types';

export default function Trainer(props) {
  return(
    <div className="trainer">
        <p>Name: {props.name}</p>
        <p>Age: {props.age}</p>
        <p>Trainer: {props.isTrainer ? 'Yes' : 'No'}</p>
    </div>
  );
}

// Check data type 
Trainer.propTypes = {
    name: PropTypes.string,
    age: PropTypes.number,
    istrainer: PropTypes.bool,
}

// default props
Trainer.defaultProps = {
    name: 'Guest',
    age: 0,
    istrainer: false,
}
