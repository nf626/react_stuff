import Card from "./Card";
import Card2 from "./Card2";
import Header from './Header';
import Footer from './Footer';
import Food from './Food';
import Button from "./Button";
import Trainer from "./Student";

function App() {
  return(
    <>
      <Header></Header>
      <Card></Card>
      <Trainer name='Red' age={10} isTrainer={true}></Trainer>
      <Card2></Card2>
      <Trainer name='Blue' age={10} isTrainer={false}></Trainer>
      <Trainer name='Green' age={10} isTrainer={true}></Trainer>
      <Button></Button>
      <Footer></Footer>
    </>
  );
}

export default App
