import { useDisclosure } from "@mantine/hooks";
import {
  Modal,
  Button,
  Container,
  Select,
  Group,
  Textarea,
} from "@mantine/core";
import axios from "axios";
import { useState } from "react";

export function Text2Audio() {
  const [opened, { open, close }] = useDisclosure(false);
  const [audioUrl, setAudioUrl] = useState("");

  async function handleOnSubmitForm(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const text = formData.get("text");
    const lang = formData.get("lang");

//     const response = await axios.post('/api/text2audio', payload, { responseType: 'blob' });
// const url = URL.createObjectURL(response.data);

    try {
      const response = await axios.post(
        "http://localhost:8000/text2audio", {
        text: text,
        lang: lang,
      }, { responseType: 'blob' });
      // const blob = response.data;

      const url = URL.createObjectURL(response.data);
      setAudioUrl(url);
    } catch (error) {
      console.error("Lỗi khi POST dữ liệu:", error);
    } finally {
    }
  }

  return (
    <>
      <Modal
        opened={opened}
        onClose={close}
        fullScreen
        radius={0}
        transitionProps={{ transition: "fade", duration: 200 }}
      >
        <Container>
          <form onSubmit={handleOnSubmitForm}>
            <Textarea
              label="Text"
              placeholder="Enter your text here..."
              autosize
              name="text"
              minRows={4}
              maxRows={6}
            />
            <Select
              label="Language"
              placeholder="Pick value"
              defaultValue="vi"
              name="lang"
              data={["en", "vi"]}
            />
            <Group justify="center" mt="xl">
              <Button variant="filled" type="submit">Convert</Button>
            </Group>
          </form>
          {audioUrl && (
            <div style={{ marginTop: "15px" }}>
              <audio src={audioUrl} controls autoPlay />
            </div>
          )}
        </Container>
      </Modal>

      <Button variant="default" onClick={open}>
        Convert text to audio
      </Button>
    </>
  );
}
