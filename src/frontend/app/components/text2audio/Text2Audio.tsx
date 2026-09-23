import { useDisclosure } from '@mantine/hooks';
import {Modal, Button, Container, Select, Group, Textarea} from '@mantine/core';

export function Text2Audio() {
  const   [opened, { open, close }] = useDisclosure(false);

  function handleOnClick(event) {
    open()

  }
  return (
    <>
      <Modal
        opened={opened}
        onClose={close}
        fullScreen
        radius={0}
        transitionProps={{ transition: 'fade', duration: 200 }}
      >
        <Container>

          <Textarea
            label="Text"
            placeholder="Enter your text here..."
            autosize
            minRows={4}
            maxRows={6}
        />
                    <Select
            label="Language"
            placeholder="Pick value"
            defaultValue="vi"
            data={['en', 'vi']}
          />
        <Group justify="center" mt="xl">
          <Button variant="filled">Convert</Button>
        </Group>

        </Container>
      </Modal>

      <Button variant="default" onClick={open}>
        Convert text to audio
      </Button>
    </>
  );
}