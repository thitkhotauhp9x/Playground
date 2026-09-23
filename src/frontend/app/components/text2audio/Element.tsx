import { useDisclosure } from '@mantine/hooks';
import {Modal, Button, Container, Select, Group, Textarea} from '@mantine/core';

function Demo() {
  const [opened, { open, close }] = useDisclosure(false);

  return (
    <>
      <Modal
        opened={opened}
        onClose={close}
        title="This is a fullscreen modal"
        fullScreen
        radius={0}
        transitionProps={{ transition: 'fade', duration: 200 }}
      >
        <Container>
          <Select
            label="Language"
            placeholder="Pick value"
            defaultValue="vi"
            data={['en', 'vi']}
          />
        <Group justify="center" mt="xl">
          <Button variant="filled">Submit</Button>

        </Group>
        <Textarea
            label="Text"
            placeholder="Enter your text here..."
            autosize
            minRows={4}
            maxRows={6}
        />
        </Container>
      </Modal>

      <Button variant="default" onClick={open}>
        Open modal
      </Button>
    </>
  );
}