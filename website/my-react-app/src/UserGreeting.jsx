
export default function UserGreeting(props) {
    const welcomeMessage = <h2 className="welcome-message">Welcome {props.username}</h2>
    const prompt = <h2 className="prompt">Please log in to continue</h2>

    if (props.isLoggedIn) {
        return welcomeMessage;
    } else {
        return prompt;
    }
}
