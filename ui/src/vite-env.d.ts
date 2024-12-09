/// <reference types="vite/client" />
declare module '@primevue/forms' {
  export * from '@primevue/forms/form';
  export interface FormSlotsFixed {
    /**
     * Default content slot.
     * @param {Object} scope - default slot's params.
     */
    default: (
      scope: {
        /**
         * Registers a form field for validation and tracking.
         * @param field - The name of the form field to register.
         * @param options - Configuration options for the field, such as validation rules.
         * @returns - Returns an object or value representing the registered field.
         */
        register: (field: string, options: any) => any;
        /**
         * Resets the entire form state, clearing values and validation statuses.
         */
        reset: () => void;
        /**
         * Indicates whether the form is valid, returning `true` if all fields pass validation.
         */
        valid: boolean;
      } & Record<string, FormFieldState>
    ) => VNode[];
  }
  export declare const Form: DefineComponent<FormProps, FormSlotsFixed, FormEmits>;

  export * from '@primevue/forms/form/style';
  export { default as FormStyle } from '@primevue/forms/form/style';

  // FormField
  export * from '@primevue/forms/formfield';
  export { default as FormField } from '@primevue/forms/formfield';
  export * from '@primevue/forms/formfield/style';
  export { default as FormFieldStyle } from '@primevue/forms/formfield/style';
}
