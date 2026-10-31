import { useDisclosure } from "@mantine/hooks";
import { Dialog, Group, Button, Text, Textarea } from "@mantine/core";
import { InputWithButton } from "@/app/components/conversation/InputWithButton";
import { useState } from "react";

export function ConversationDialog() {
  const [messages, setMessages] = useState([]);

  const [opened, { toggle, close }] = useDisclosure(false);

  return (
    <>
      <Group justify="center">
        <Button onClick={toggle}>Toggle dialog</Button>
      </Group>

      <Dialog
        opened={opened}
        withCloseButton
        onClose={close}
        size="lg"
        position={{ bottom: 20, left: 20 }}
      >
        <Text size="sm" mb="xs" fw={500}>
          Subscribe to email newsletter
        </Text>
        <Textarea label="User" placeholder="Hello you" disabled />
        <Textarea label="Assistance" placeholder="Nice to meet you" disabled />
        <InputWithButton />
      </Dialog>
    </>
  );
}
