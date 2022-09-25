import {useState} from "react";
import axios from "axios";
import {Button, Container, Form} from "react-bootstrap";

function App() {

    const int_to_front = {
        0: 'light',
        1: 'success'
    }

    const [colorValues, setColorValues] = useState({
        'financas': 'light',
        'educacao': 'light',
        'industrias': 'light',
        'varejo': 'light',
        'orgao_publico': 'light',
    });
    const [currentSentence, setCurrentSentence] = useState("");

    const categories = ['financas', 'educacao', 'industrias', 'varejo', 'orgao_publico'];

    function submitToAPI(event) {
        axios({
            method: "POST",
            url: "http://localhost:8000/",
            data: {
                sentence: currentSentence
            }
        })
            .then((response) => {
                let received_data = response.data;
                let new_values = {};
                for (let category of categories) {
                    new_values[category] = int_to_front[received_data[category]];
                }
                // noinspection JSCheckFunctionSignatures
                setColorValues(new_values);
            })
        event.preventDefault()
    }

    return (
        <Container fluid="md">
            <h1 className="mt-3">Classificador de Frases por Setor</h1>

            <p>A frase pode ser classificada em 1 ou mais dos seguintes grupos:</p>
            <ul>
                <li>Finanças</li>
                <li>Educação</li>
                <li>Indústrias</li>
                <li>Varejo</li>
                <li>Órgão Público</li>
            </ul>

            <Form>
                <Form.Group className="mb-3">
                    <Form.Label>Frase</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Digite a frase"
                        id="sentence"
                        value={currentSentence}
                        onChange={(event) => {
                            setCurrentSentence(event.target.value);
                        }}
                    />
                </Form.Group>

                <Button variant="primary" type="submit" onClick={submitToAPI}>
                    Classificar frase
                </Button>
            </Form>

            <p className="mt-3">O resultado das categorias que a frase pertence é indicado em verde:</p>

            <Button variant={colorValues['financas']}>Finanças</Button>{' '}
            <Button variant={colorValues['educacao']}>Educação</Button>{' '}
            <Button variant={colorValues['industrias']}>Indústrias</Button>{' '}
            <Button variant={colorValues['varejo']}>Varejo</Button>{' '}
            <Button variant={colorValues['orgao_publico']}>Órgão Público</Button>{' '}
        </Container>
    );
}

export default App;