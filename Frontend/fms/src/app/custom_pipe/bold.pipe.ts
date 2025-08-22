import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Pipe({
  name: 'bold'
})
export class BoldPipe implements PipeTransform {

  constructor(private sanitizer: DomSanitizer) {}

  transform(value: any): SafeHtml {
    if (!value) {
      return '';
    }
    const boldedValue = `<strong>${value}</strong>`;
    return this.sanitizer.bypassSecurityTrustHtml(boldedValue);
  }
}