import { IconArrowRight } from '@tabler/icons-react';
import { ActionIcon, TextInput, TextInputProps, useMantineTheme } from '@mantine/core';

export function InputWithButton(props: TextInputProps) {
  const theme = useMantineTheme();

  function handleOnClick() {

  }

  return (
    <TextInput
      radius="xl"
      size="md"
      placeholder="Search questions"
      rightSection={
        <ActionIcon
          size={32}
          radius="xl"
          color={theme.primaryColor}
          variant="filled"
          aria-label="Search"
          onClick={handleOnClick}
        >
          <IconArrowRight size={18} stroke={1.5} />
        </ActionIcon>
      }
      aria-label="Search questions"
      {...props}
    />
  );
}
